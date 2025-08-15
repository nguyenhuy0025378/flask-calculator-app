#!/bin/bash

# Docker Container Management Script for Flask Calculator App
# This script provides easy commands to build, start, stop, and manage the Docker containers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to build and start containers
start_containers() {
    print_info "Building and starting Flask Calculator containers..."
    
    # Build the images
    docker-compose build
    
    # Start the containers in detached mode
    docker-compose up -d
    
    print_info "Waiting for services to be ready..."
    sleep 5
    
    # Check if the calculator service is healthy
    if docker-compose ps | grep -q "calculator.*healthy"; then
        print_info "✅ Flask Calculator is running at: http://localhost:8080"
    else
        print_warning "Flask Calculator is starting up..."
        print_info "Check status with: $0 status"
    fi
    
    
    echo ""
    print_info "Use '$0 logs' to view logs"
    print_info "Use '$0 stop' to stop all containers"
}

# Function to stop containers
stop_containers() {
    print_info "Stopping all containers..."
    docker-compose down
    print_info "All containers stopped."
}

# Function to restart containers
restart_containers() {
    print_info "Restarting containers..."
    docker-compose restart
    print_info "Containers restarted."
}

# Function to view logs
view_logs() {
    if [ -z "$1" ]; then
        docker-compose logs -f
    else
        docker-compose logs -f "$1"
    fi
}

# Function to show status
show_status() {
    print_info "Container status:"
    docker-compose ps
}

# Function to rebuild containers
rebuild_containers() {
    print_info "Rebuilding containers..."
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    print_info "Containers rebuilt and started."
}

# Function to clean up
cleanup() {
    print_warning "This will remove all containers and images for this project."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down --rmi all
        print_info "Cleanup complete."
    else
        print_info "Cleanup cancelled."
    fi
}

# Function to run tests
run_tests() {
    print_info "Running tests inside the calculator container..."
    docker-compose exec calculator pytest -v
}

# Function to access shell
access_shell() {
    print_info "Accessing calculator container shell..."
    docker-compose exec calculator /bin/sh
}

# Main script logic
check_docker

case "${1:-start}" in
    start)
        start_containers
        ;;
    stop)
        stop_containers
        ;;
    restart)
        restart_containers
        ;;
    logs)
        view_logs "$2"
        ;;
    status)
        show_status
        ;;
    rebuild)
        rebuild_containers
        ;;
    test)
        run_tests
        ;;
    shell)
        access_shell
        ;;
    clean)
        cleanup
        ;;
    *)
        echo "Flask Calculator Docker Manager"
        echo "================================"
        echo "Usage: $0 {start|stop|restart|logs|status|rebuild|test|shell|clean}"
        echo ""
        echo "Commands:"
        echo "  start    - Build and start all containers (default)"
        echo "  stop     - Stop all containers"
        echo "  restart  - Restart all containers"
        echo "  logs     - View container logs (optional: service name)"
        echo "  status   - Show container status"
        echo "  rebuild  - Rebuild and restart containers"
        echo "  test     - Run tests inside the container"
        echo "  shell    - Access calculator container shell"
        echo "  clean    - Remove all containers, volumes, and images"
        echo ""
        echo "Examples:"
        echo "  $0              # Start containers (default)"
        echo "  $0 start        # Start containers"
        echo "  $0 logs         # View all logs"
        echo "  $0 logs calculator  # View calculator logs only"
        echo "  $0 stop         # Stop all containers"
        exit 1
        ;;
esac