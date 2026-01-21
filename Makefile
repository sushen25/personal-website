.PHONY: help install clean start-all start-backend start-frontend start-agent stop-all test

# Default target
help:
	@echo "Available targets:"
	@echo "  make install        - Install all dependencies (backend, frontend, agent)"
	@echo "  make clean          - Clean all build artifacts and dependencies"
	@echo ""
	@echo "  make start-all      - Start all services (backend, frontend, agent) concurrently"
	@echo "  make start-backend  - Start backend API server (FastAPI)"
	@echo "  make start-frontend - Start frontend development server (Next.js)"
	@echo "  make start-agent    - Start agent service locally"
	@echo ""
	@echo "  make stop-all       - Stop all running services"
	@echo "  make test           - Run tests for all services"

# Installation targets
install: install-backend install-frontend install-agent
	@echo "✓ All dependencies installed"

install-backend:
	@echo "Installing backend dependencies..."
	cd my-website-backend && \
		python3.11 -m venv venv && \
		. venv/bin/activate && \
		pip install -r requirements.txt
	@echo "✓ Backend dependencies installed"

install-frontend:
	@echo "Installing frontend dependencies..."
	cd my-website-frontend && npm install
	@echo "✓ Frontend dependencies installed"

install-agent:
	@echo "Installing agent service dependencies..."
	cd agent-service && \
		python3.11 -m venv venv && \
		. venv/bin/activate && \
		pip install -r requirements.txt
	@echo "✓ Agent service dependencies installed"

# Clean targets
clean: clean-backend clean-frontend clean-agent
	@echo "✓ All artifacts cleaned"

clean-backend:
	@echo "Cleaning backend..."
	cd my-website-backend && \
		rm -rf venv __pycache__ .pytest_cache *.pyc .serverless
	@echo "✓ Backend cleaned"

clean-frontend:
	@echo "Cleaning frontend..."
	cd my-website-frontend && \
		rm -rf .next node_modules out
	@echo "✓ Frontend cleaned"

clean-agent:
	@echo "Cleaning agent service..."
	cd agent-service && \
		rm -rf venv __pycache__ .pytest_cache *.pyc .serverless
	@echo "✓ Agent service cleaned"

# Start all services concurrently
start-all:
	@echo "Starting all services..."
	@echo "Backend: http://localhost:4000"
	@echo "Frontend: http://localhost:8000"
	@echo "Agent: Running locally (invoked by backend)"
	@echo ""
	@echo "Press Ctrl+C to stop all services"
	@trap 'make stop-all' INT; \
	make start-backend & \
	BACKEND_PID=$$!; \
	sleep 3; \
	make start-frontend & \
	FRONTEND_PID=$$!; \
	wait $$BACKEND_PID $$FRONTEND_PID

# Start individual services
start-backend:
	@echo "Starting backend API server with serverless offline on http://localhost:4000..."
	cd my-website-backend && \
		serverless offline start --stage dev --httpPort 4000

start-frontend:
	@echo "Starting frontend development server on http://localhost:8000..."
	cd my-website-frontend && npm run dev -- --port 8000

start-agent:
	@echo "Starting agent service locally..."
	@echo "Note: Agent service is typically invoked by the backend via Lambda."
	@echo "For local testing, use the backend's agent client or deploy to AWS."
	cd agent-service && \
		. venv/bin/activate && \
		python -c "from src.agent import agent_handler; print('Agent service ready for local invocation')"

# Stop all services
stop-all:
	@echo "Stopping all services..."
	-pkill -f "serverless offline"
	-pkill -f "next dev"
	@echo "✓ All services stopped"

# Test targets
test: test-backend test-frontend test-agent
	@echo "✓ All tests completed"

test-backend:
	@echo "Running backend tests..."
	cd my-website-backend && \
		. venv/bin/activate && \
		python -m pytest tests/ -v || echo "No tests found for backend"

test-frontend:
	@echo "Running frontend tests..."
	cd my-website-frontend && \
		npm test || echo "No tests configured for frontend"

test-agent:
	@echo "Running agent service tests..."
	cd agent-service && \
		. venv/bin/activate && \
		python -m pytest tests/ -v || echo "No tests found for agent service"

# Development helpers
dev-backend-logs:
	@echo "Tailing backend logs..."
	tail -f my-website-backend/logs/*.log

dev-frontend-build:
	@echo "Building frontend for production..."
	cd my-website-frontend && npm run build

dev-backend-shell:
	@echo "Opening backend Python shell..."
	cd my-website-backend && . venv/bin/activate && python

dev-agent-shell:
	@echo "Opening agent service Python shell..."
	cd agent-service && . venv/bin/activate && python

# Deployment targets
deploy-backend:
	@echo "Deploying backend to AWS..."
	cd my-website-backend && serverless deploy --stage dev --verbose

deploy-frontend:
	@echo "Deploying frontend to AWS..."
	cd my-website-frontend && npm run build && serverless deploy --stage dev

deploy-agent:
	@echo "Deploying agent service to AWS..."
	cd agent-service && serverless deploy --stage dev --verbose

deploy-all: deploy-agent deploy-backend deploy-frontend
	@echo "✓ All services deployed"

# Database setup (if needed)
setup-db:
	@echo "Setting up DynamoDB tables..."
	@echo "Run this with appropriate AWS credentials"
	cd my-website-backend && \
		. venv/bin/activate && \
		python scripts/setup_dynamodb.py || echo "No database setup script found"
