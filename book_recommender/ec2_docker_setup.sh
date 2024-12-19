sudo apt update && sudo apt upgrade -y && sudo apt install -y docker.io && sudo apt install -y unzip
sudo systemctl start docker
sudo systemctl enable docker

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install