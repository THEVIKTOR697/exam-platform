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

                systemctl start docker
                systemctl enable docker

                usermod -aG docker ec2-user

                cd /home/ec2-user
                git clone https://github.com/THEVIKTOR697/exam-platform.git
                cd exam-platform

                # DEBUG
                ls -la

                docker build -t exam-platform .
                docker run -d -p 8000:8000 exam-platform
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
