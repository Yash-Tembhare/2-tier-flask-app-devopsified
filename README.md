# 🚀 Automated CI/CD Pipeline for 2-Tier Flask Application

## 📋 Project Summary
Built a complete CI/CD pipeline that automatically deploys a Flask web application with MySQL database using Docker containers on AWS EC2, orchestrated by Jenkins.

---

## 🏗️ Architecture
```
Developer → GitHub → Jenkins → Docker → Flask App + MySQL
```

**Flow:**
1. Code pushed to GitHub
2. Jenkins detects changes
3. Builds Docker images
4. Deploys containers automatically
5. Application live on AWS EC2

---

## 🛠️ Technologies Used
- **Cloud:** AWS EC2 (Ubuntu 22.04)
- **CI/CD:** Jenkins
- **Containerization:** Docker, Docker Compose
- **Application:** Flask (Python)
- **Database:** MySQL 8.0
- **Version Control:** Git, GitHub

---

## ⚙️ What We Did

### 1. AWS EC2 Setup
- Launched t2.medium Ubuntu instance
- Configured Security Groups (ports: 22, 80, 5000, 8080, 3306)
- Connected via SSH

### 2. Installed Dependencies
```bash
- Git
- Docker & Docker Compose
- Java (OpenJDK 17)
- Jenkins
```

### 3. Jenkins Configuration
- Installed Jenkins on EC2
- Configured Docker permissions for Jenkins
- Created pipeline job with GitHub integration
- Set up automated builds

### 4. Application Structure
**Key Files:**
- `Dockerfile` - Flask app container definition
- `docker-compose.yml` - Multi-container orchestration
- `Jenkinsfile` - CI/CD pipeline stages
- `app.py` - Flask application code
- `requirements.txt` - Python dependencies

### 5. Pipeline Stages
```groovy
1. Clone Code - Pull from GitHub
2. Build Docker Image - Create Flask container
3. Deploy - Start containers with docker-compose
```

---

## 🔧 Key Changes Made

### Initial Issues & Fixes

**1. Docker Compose Health Check Timeout**
- **Problem:** MySQL health check caused build to hang indefinitely
- **Fix:** Removed `condition: service_healthy` and health checks
- **Result:** Build completed in 2-3 minutes

**2. MySQL Volume Corruption**
- **Problem:** MySQL container kept restarting with data corruption errors
- **Error:** `Cannot create redo log files because data files are corrupt`
- **Fix:** Removed corrupted volume with `docker volume rm`
- **Result:** Fresh MySQL initialization successful

**3. EC2 Instance Freezing**
- **Problem:** t2.micro (1GB RAM) insufficient for Docker + Jenkins
- **Fix:** Upgraded to t2.medium (4GB RAM)
- **Result:** Stable performance during builds

**4. Git Remote Configuration**
- **Problem:** Wrong remote repository URL
- **Fix:** Updated remote with `git remote set-url origin`
- **Result:** Successful code push to GitHub

**5. Connection Issues**
- **Problem:** ERR_SSL_PROTOCOL_ERROR when accessing Jenkins
- **Fix:** Used `http://` instead of `https://`
- **Result:** Jenkins accessible on port 8080

**6. Public IP Changes**
- **Problem:** IP changed after EC2 stop/restart
- **Fix:** Used new public IP for all connections
- **Note:** Recommended Elastic IP for production

---

## 📊 Final Configuration

### docker-compose.yml (Optimized)
```yaml
version: "3.8"

services:
  mysql:
    container_name: mysql
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: "root"
      MYSQL_DATABASE: "flask_db"
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - two-tier-nt

  flask-app:
    container_name: two-tier-flask-app
    build:
      context: .
    ports:
      - "5000:5000"
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_USER=root
      - MYSQL_PASSWORD=root
      - MYSQL_DB=flask_db
    networks:
      - two-tier-nt
    depends_on:
      - mysql
    restart: always

volumes:
  mysql_data:

networks:
  two-tier-nt:
```

### Security Group Rules
| Type | Port | Source | Purpose |
|------|------|--------|---------|
| SSH | 22 | My IP | SSH access |
| HTTP | 80 | 0.0.0.0/0 | Web traffic |
| Custom TCP | 5000 | 0.0.0.0/0 | Flask app |
| Custom TCP | 8080 | 0.0.0.0/0 | Jenkins |
| Custom TCP | 3306 | 0.0.0.0/0 | MySQL |

---

## 🎯 Output & Results

### ✅ Successful Deployment
- **Jenkins Pipeline:** All 3 stages completed successfully
- **Containers:** 2 containers running (Flask + MySQL)
- **Application:** Accessible at `http://EC2_PUBLIC_IP:5000`
- **Database:** MySQL initialized with `flask_db` database
- **Build Time:** 2-3 minutes per deployment

### Verification Commands
```bash
# Check running containers
docker ps

# View Flask logs
docker logs two-tier-flask-app

# View MySQL logs
docker logs mysql

# Test application locally
curl http://localhost:5000
```

---

## 📚 What We Learned

### Technical Skills
1. **AWS EC2 Management**
   - Instance configuration and security groups
   - SSH access and troubleshooting
   - Resource sizing (t2.micro vs t2.medium)

2. **Docker & Containerization**
   - Writing Dockerfiles
   - Multi-container orchestration with docker-compose
   - Volume management and persistence
   - Container networking
   - Troubleshooting container crashes

3. **Jenkins CI/CD**
   - Pipeline as code (Jenkinsfile)
   - SCM integration with GitHub
   - Build automation
   - Docker permissions for Jenkins user

4. **DevOps Best Practices**
   - Infrastructure as Code (IaC)
   - Automated deployments
   - Environment variable management
   - Service dependencies handling

### Problem-Solving Skills
- Debugging container failures using logs
- Resolving permission issues (Docker group)
- Handling corrupted volumes
- Optimizing configurations for reliability
- SSH and network troubleshooting

### Key Takeaways
- ⚡ Health checks can cause timeouts - use simple `depends_on` for basic setups
- 💾 Always clean up corrupted volumes before redeployment
- 🔒 Proper security group configuration is critical
- 🎯 Instance sizing matters - match resources to workload
- 🔄 CI/CD saves time and reduces human error

---

## 🐛 Troubleshooting Guide

### Common Issues & Solutions

**Build Hangs at "Deploy" Stage**
```bash
# Remove health check dependencies from docker-compose.yml
# Cancel stuck build in Jenkins
# Clean up: docker compose down -v
# Rebuild
```

**MySQL Container Keeps Restarting**
```bash
# Check logs: docker logs mysql
# Remove corrupted volume: docker volume rm <volume_name>
# Restart: docker compose up -d
```

**Cannot Connect to EC2**
```bash
# Verify instance is running
# Check security group has port 22 open
# Use correct public IP (changes after stop/start)
# Fix PEM permissions: chmod 400 key.pem
```

**Jenkins Shows 404 or Connection Refused**
```bash
# Use http:// not https://
# Check Jenkins service: sudo systemctl status jenkins
# Verify security group allows port 8080
```

**Docker Permission Denied in Jenkins**
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

---

## 🚀 How to Use This Project

### Prerequisites
- AWS Account
- GitHub Account
- Basic Linux knowledge
- SSH client (PuTTY/Terminal)

### Quick Start
1. **Clone Repository**
   ```bash
   git clone https://github.com/Yash-Tembhare/2-tier-flask-app-devopsified.git
   ```

2. **Launch EC2 Instance**
   - Ubuntu 22.04, t2.medium
   - Configure security groups
   - Connect via SSH

3. **Run Setup Script**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install dependencies
   sudo apt install git docker.io docker-compose-v2 openjdk-17-jdk -y
   
   # Install Jenkins
   # (Follow Jenkins installation steps)
   ```

4. **Configure Jenkins**
   - Access: `http://EC2_IP:8080`
   - Create pipeline job
   - Link to GitHub repository
   - Build and deploy

5. **Access Application**
   ```
   http://EC2_IP:5000
   ```

---

## 📈 Future Improvements

- [ ] Implement GitHub Webhooks for auto-trigger builds
- [ ] Add automated testing stage in pipeline
- [ ] Set up monitoring with Prometheus & Grafana
- [ ] Implement SSL/TLS certificates (HTTPS)
- [ ] Use AWS RDS instead of containerized MySQL
- [ ] Add email notifications for build status
- [ ] Implement blue-green deployment strategy
- [ ] Use Elastic IP for consistent access
- [ ] Add environment-specific configurations (dev/prod)
- [ ] Implement secrets management (AWS Secrets Manager)

---

## 📝 Project Files

```
project-root/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Flask container definition
├── docker-compose.yml    # Multi-container setup
├── Jenkinsfile          # CI/CD pipeline definition
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

---

## 👨‍💻 Author
**Yash Tembhare**
- GitHub: [@Yash-Tembhare](https://github.com/Yash-Tembhare)
- Project: [2-tier-flask-app-devopsified](https://github.com/Yash-Tembhare/2-tier-flask-app-devopsified)

---

## 📅 Project Timeline
**Duration:** 1 Day  
**Date:** December 11-12, 2025  
**Status:** ✅ Completed & Deployed

---

## 🙏 Acknowledgments
- AWS Documentation
- Jenkins Documentation
- Docker Documentation
- DevOps Community

---

## 📄 License
This project is open source and available for educational purposes.

---

**⭐ If you found this helpful, please star the repository!**

**🔗 Live Demo:** `http://YOUR_EC2_IP:5000`