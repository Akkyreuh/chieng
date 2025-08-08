@echo off
echo Setting up Dog Breed Classifier Development Environment
echo.

echo Step 1: Building and starting services with Docker Compose...
docker-compose up --build -d

echo.
echo Step 2: Waiting for services to start...
timeout /t 10 /nobreak > nul

echo.
echo Step 3: Checking service health...
docker-compose ps

echo.
echo Setup complete!
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo To stop services: docker-compose down
echo To view logs: docker-compose logs -f
echo.
pause
