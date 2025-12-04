terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}
provider "aws" { region = "us-east-1" }
resource "aws_security_group" "chatbot_sg" {
  name = "talentscout-sg"
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 22
    to_port     = 22
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
resource "aws_instance" "chatbot" {
  ami           = "ami-053b0d53c279acc90"
  instance_type = "t2.micro"
  key_name      = "aws-key"
  vpc_security_group_ids = [aws_security_group.chatbot_sg.id]
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y python3-pip git
              git clone https://github.com/dhairyashild/talent-scout-chatbot.git
              cd talent-scout-chatbot
              pip3 install -r requirements.txt
              nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
              EOF
  tags = { Name = "TalentScout-Chatbot" }
}
output "public_ip" { value = aws_instance.chatbot.public_ip }
output "app_url" { value = "http://${aws_instance.chatbot.public_ip}:8501" }
