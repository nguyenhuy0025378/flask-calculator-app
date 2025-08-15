#!/bin/bash

# AWS ECS Setup Script for Calculator App
# Run these commands to set up the AWS infrastructure

set -e

# Variables - Update these with your values
AWS_REGION="ap-southeast-1"
ECR_REPOSITORY="calculator-app"
ECS_CLUSTER="calculator-cluster"
ECS_SERVICE="calculator-service"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "Setting up AWS infrastructure for Calculator App"
echo "Account ID: $ACCOUNT_ID"
echo "Region: $AWS_REGION"

# 1. Create ECR Repository
echo "Creating ECR repository..."
aws ecr create-repository \
    --repository-name $ECR_REPOSITORY \
    --region $AWS_REGION \
    --image-scanning-configuration scanOnPush=true \
    --encryption-configuration encryptionType=AES256 || echo "Repository might already exist"

# 2. Create ECS Cluster
echo "Creating ECS cluster..."
aws ecs create-cluster \
    --cluster-name $ECS_CLUSTER \
    --capacity-providers FARGATE \
    --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1 \
    --region $AWS_REGION || echo "Cluster might already exist"

# 3. Create CloudWatch Log Group
echo "Creating CloudWatch log group..."
aws logs create-log-group \
    --log-group-name "/ecs/calculator-app" \
    --region $AWS_REGION || echo "Log group might already exist"

# 4. Create IAM Role for ECS Task Execution
echo "Creating ECS Task Execution Role..."
cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

aws iam create-role \
    --role-name ecsTaskExecutionRole \
    --assume-role-policy-document file://trust-policy.json || echo "Role might already exist"

aws iam attach-role-policy \
    --role-name ecsTaskExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# 5. Create IAM Role for ECS Task (application permissions)
echo "Creating ECS Task Role..."
aws iam create-role \
    --role-name ecsTaskRole \
    --assume-role-policy-document file://trust-policy.json || echo "Role might already exist"

# 6. Update task definition with correct account ID
echo "Updating task definition with account ID..."
sed "s/ACCOUNT_ID/$ACCOUNT_ID/g" .aws/task-definition.json > .aws/task-definition-updated.json

# 7. Register ECS Task Definition
echo "Registering ECS task definition..."
aws ecs register-task-definition \
    --cli-input-json file://.aws/task-definition-updated.json \
    --region $AWS_REGION

# 8. Create VPC and Security Group (if needed)
echo "Setting up VPC and Security Group..."

# Get default VPC
VPC_ID=$(aws ec2 describe-vpcs \
    --filters "Name=isDefault,Values=true" \
    --query "Vpcs[0].VpcId" \
    --output text \
    --region $AWS_REGION)

# Get subnets
SUBNET_IDS=$(aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values=$VPC_ID" \
    --query "Subnets[*].SubnetId" \
    --output text \
    --region $AWS_REGION)

# Create security group
SG_ID=$(aws ec2 create-security-group \
    --group-name calculator-app-sg \
    --description "Security group for Calculator App" \
    --vpc-id $VPC_ID \
    --region $AWS_REGION \
    --query "GroupId" \
    --output text) || SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=calculator-app-sg" \
    --query "SecurityGroups[0].GroupId" \
    --output text \
    --region $AWS_REGION)

# Allow HTTP traffic
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 8080 \
    --cidr 0.0.0.0/0 \
    --region $AWS_REGION || echo "Security group rule might already exist"

# 9. Create ECS Service
echo "Creating ECS service..."
cat > service-definition.json << EOF
{
  "serviceName": "$ECS_SERVICE",
  "cluster": "$ECS_CLUSTER",
  "taskDefinition": "calculator-task-def",
  "desiredCount": 1,
  "launchType": "FARGATE",
  "networkConfiguration": {
    "awsvpcConfiguration": {
      "subnets": ["$(echo $SUBNET_IDS | cut -d' ' -f1)", "$(echo $SUBNET_IDS | cut -d' ' -f2)"],
      "securityGroups": ["$SG_ID"],
      "assignPublicIp": "ENABLED"
    }
  },
  "healthCheckGracePeriodSeconds": 300
}
EOF

aws ecs create-service \
    --cli-input-json file://service-definition.json \
    --region $AWS_REGION || echo "Service might already exist"

# 10. Create Application Load Balancer (Optional)
echo "Creating Application Load Balancer..."
ALB_ARN=$(aws elbv2 create-load-balancer \
    --name calculator-app-alb \
    --subnets $SUBNET_IDS \
    --security-groups $SG_ID \
    --region $AWS_REGION \
    --query "LoadBalancers[0].LoadBalancerArn" \
    --output text) || echo "Load balancer might already exist"

# Clean up temporary files
rm -f trust-policy.json service-definition.json .aws/task-definition-updated.json

echo ""
echo "AWS Setup Complete!"
echo "==================="
echo "ECR Repository URI: $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY"
echo "ECS Cluster: $ECS_CLUSTER"
echo "ECS Service: $ECS_SERVICE"
echo "Security Group ID: $SG_ID"
echo ""
echo "Next steps:"
echo "1. Add these GitHub Secrets:"
echo "   AWS_ACCESS_KEY_ID"
echo "   AWS_SECRET_ACCESS_KEY"
echo "   SONAR_TOKEN"
echo "   SONAR_HOST_URL"
echo ""
echo "2. Push your code to trigger the CI/CD pipeline"
echo "3. Monitor the deployment in AWS ECS console"