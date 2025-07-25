name: React (Vite) CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'

      - name: Install dependencies
        run: npm install

      - name: Build React App (Vite)
        run: npm run build

      - name: Run tests
        run: npm run test


  docker-build-and-push:
    needs: build-and-test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Docker login to Docker Hub
        run: |
          docker login -u "${{ secrets.DOCKERHUB_USERNAME }}" -p "${{ secrets.DOCKERHUB_TOKEN }}"

      - name: Build Docker image
        run: docker build -t "${{ secrets.DOCKERHUB_USERNAME }}/greeting-react-app:latest" .

      - name: Push Docker image to Docker Hub
        run: docker push "${{ secrets.DOCKERHUB_USERNAME }}/greeting-react-app:latest"      
