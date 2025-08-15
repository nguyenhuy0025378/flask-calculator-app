# AWS ECS Deployment Guide

This document explains how to deploy the Flask Calculator app to AWS ECS with complete CI/CD pipeline.

## Architecture Overview

```
GitHub → GitHub Actions → ECR → ECS Fargate → ALB → Internet
```

- **ECR**: Container registry storing Docker images
- **ECS**: Container orchestration service running our app
- **ALB**: Application Load Balancer routing traffic to containers
- **Fargate**: Serverless compute for containers

## Components Used

### ECR (Elastic Container Registry)
- Stores Docker images built by GitHub Actions
- Images tagged with git commit SHA for versioning
- Repository: `987277324727.dkr.ecr.ap-southeast-1.amazonaws.com/calculator-app`
- URL: https://ap-southeast-1.console.aws.amazon.com/ecr/repositories/private/987277324727/calculator-app?region=ap-southeast-1


### ECS (Elastic Container Service)
- **Cluster**: `calculator-cluster` - Groups related services
- **Service**: `calculator-service` - Ensures desired number of tasks running
- **Task Definition**: `calculator-task-def` - Blueprint for containers
- **Launch Type**: Fargate (serverless, AWS-managed infrastructure)
- **URL**: https://ap-southeast-1.console.aws.amazon.com/ecs/v2/clusters/calculator-cluster/services?region=ap-southeast-1
- **Log CloudWatch**: https://ap-southeast-1.console.aws.amazon.com/ecs/v2/clusters/calculator-cluster/services/calculator-service/logs?region=ap-southeast-1
- 

### ALB (Application Load Balancer)
- **Load Balancer**: `calculator-app-alb` - Internet-facing entry point
- **Target Group**: `calculator-target-group` - Routes traffic to ECS tasks
- **Health Check**: `/health` endpoint on port 8080
- **Public URL**: `http://calculator-app-alb-1153111872.ap-southeast-1.elb.amazonaws.com`

## Deployment Steps

### 1. Initial AWS Setup
```bash
# Run the setup script to create infrastructure
./aws-setup.sh
```

### 2. Configure GitHub Secrets
Add these secrets to GitHub repository:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### 3. Deploy via Git Push
```bash
git push origin main
# GitHub Actions automatically builds, pushes to ECR, and deploys to ECS
```

### 4. Configure ALB (One-time setup)
```bash
# Create target group
aws elbv2 create-target-group --name calculator-target-group --protocol HTTP --port 8080 --vpc-id $(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --region ap-southeast-1 --query "Vpcs[0].VpcId" --output text) --target-type ip --health-check-path /health --region ap-southeast-1

# Create listener 
aws elbv2 create-listener --load-balancer-arn $(aws elbv2 describe-load-balancers --names calculator-app-alb --region ap-southeast-1 --query 'LoadBalancers[0].LoadBalancerArn' --output text) --protocol HTTP --port 80 --default-actions Type=forward,TargetGroupArn=$(aws elbv2 describe-target-groups --names calculator-target-group --region ap-southeast-1 --query 'TargetGroups[0].TargetGroupArn' --output text) --region ap-southeast-1

# Link ECS service to ALB
aws ecs update-service --cluster calculator-cluster --service calculator-service --load-balancers targetGroupArn=$(aws elbv2 describe-target-groups --names calculator-target-group --region ap-southeast-1 --query 'TargetGroups[0].TargetGroupArn' --output text),containerName=calculator,containerPort=8080 --region ap-southeast-1

# Allow HTTP traffic to ALB
aws ec2 authorize-security-group-ingress --group-id sg-095038d344d29b530 --protocol tcp --port 80 --cidr 0.0.0.0/0 --region ap-southeast-1
```

## Monitoring & Debugging Commands

### Check ECS Service Status
```bash
aws ecs describe-services --cluster calculator-cluster --services calculator-service --region ap-southeast-1
```

### View Container Logs
```bash
aws logs tail /ecs/calculator-app --since 1h --region ap-southeast-1
```

### Check ALB Health
```bash
# Target health
aws elbv2 describe-target-health --target-group-arn $(aws elbv2 describe-target-groups --names calculator-target-group --region ap-southeast-1 --query 'TargetGroups[0].TargetGroupArn' --output text) --region ap-southeast-1

# ALB listeners
aws elbv2 describe-listeners --load-balancer-arn $(aws elbv2 describe-load-balancers --names calculator-app-alb --region ap-southeast-1 --query 'LoadBalancers[0].LoadBalancerArn' --output text) --region ap-southeast-1
```

### Test Application
```bash
# Health check
curl http://calculator-app-alb-1153111872.ap-southeast-1.elb.amazonaws.com/health

# Calculator API
curl -X POST http://calculator-app-alb-1153111872.ap-southeast-1.elb.amazonaws.com/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "+", "a": 5, "b": 3}'

# Web interface
open http://calculator-app-alb-1153111872.ap-southeast-1.elb.amazonaws.com
```

## CI/CD Pipeline

### GitHub Actions Workflow
1. **Test & Code Quality**: Run pytest, Black, Flake8
2. **Security Scan**: Trivy vulnerability scanning
3. **Build & Push**: Docker build → ECR push
4. **Deploy**: Update ECS service with new image

### Automatic Deployments
- Every push to `main` triggers deployment
- Zero-downtime rolling updates
- Health checks ensure stability
- Rollback capability via ECS

## Troubleshooting

### Common Issues
- **504 Gateway Timeout**: Check target group health and ECS task logs
- **Connection Timeout**: Verify security group rules allow port 80/8080
- **Health Check Failed**: Ensure `/health` endpoint returns 200
- **Task Won't Start**: Check CloudWatch logs for container errors

### Quick Fixes
```bash
# Restart ECS service
aws ecs update-service --cluster calculator-cluster --service calculator-service --force-new-deployment --region ap-southeast-1

# View security group rules
aws ec2 describe-security-groups --group-ids sg-095038d344d29b530 --region ap-southeast-1
```

## Resources Created

- ECR Repository: `calculator-app`
- ECS Cluster: `calculator-cluster` 
- ECS Service: `calculator-service`
- ALB: `calculator-app-alb`
- Target Group: `calculator-target-group`
- Security Group: `sg-095038d344d29b530`
- IAM Roles: `ecsTaskExecutionRole`, `ecsTaskRole`

## Cost Optimization

- **Fargate**: Pay per vCPU/memory used
- **ALB**: ~$16/month + data processing
- **ECR**: $0.10/GB/month storage
- **CloudWatch**: Logs retention costs

**Estimated monthly cost**: $20-30 for light usage

## Cleanup

```bash
# Delete ECS service
aws ecs update-service --cluster calculator-cluster --service calculator-service --desired-count 0 --region ap-southeast-1
aws ecs delete-service --cluster calculator-cluster --service calculator-service --region ap-southeast-1

# Delete other resources (ALB, ECR, etc.) via AWS Console
```