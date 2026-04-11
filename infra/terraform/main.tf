provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "api_server" {
  ami           = "ami-0c02fb55956c7d316" # Ubuntu (ejemplo)
  instance_type = "t3.micro"

  tags = {
    Name = "exam-platform-api"
  }
}