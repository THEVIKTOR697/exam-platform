provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "api_server" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"

  key_name = var.key_name

  vpc_security_group_ids = [aws_security_group.api_sg.id]

  user_data = <<-EOF
                #!/bin/bash
                set -e

                yum update -y
                yum install -y docker git
                curl -L https://download.docker.com/linux/centos/7/x86_64/stable/Packages/docker-compose-plugin-2.6.0-3.el7.x86_64.rpm -o ./compose-plugin.rpm
                yum install ./compose-plugin.rpm -y
                
                systemctl start docker
                systemctl enable docker

                usermod -aG docker ec2-user

                cd /home/ec2-user
                git clone https://github.com/THEVIKTOR697/exam-platform.git
                cd exam-platform

                # DEBUG
                ls -la

                #Wait for rds_endpoint
                sleep 40
                
                docker compose -f docker-compose.yml up --build
                EOF

  tags = {
    Name = "exam-platform-api"
  }
}

resource "aws_security_group" "api_sg" {
  name = "exam-platform-sg"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "FastAPI"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "postgres" {
  identifier = "exam-platform-db"

  engine         = "postgres"
  instance_class = "db.t3.micro"

  allocated_storage = 20

  username = "postgres"
  password = "postgres123"

  publicly_accessible = true
  skip_final_snapshot = true

  db_name = "examdb"

  vpc_security_group_ids = [aws_security_group.db_sg.id]
}

resource "aws_security_group" "db_sg" {
  name = "db-security-group"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    
    security_groups = [aws_security_group.api_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
