#!/bin/zsh

# swapfile 메모리를 할당
sudo dd if=/dev/zero of=/swapfile bs=128M count=16

# swapfile 권한 세팅 (READ, WRITE)
sudo chmod 600 /swapfile

# swap 공간 생성 (Make swap)
sudo mkswap /swapfile

# # /etc/fstab vi 에디터 열기
# sudo vi /etc/fstab

# # 파일의 맨 끝 다음줄에 아래 명령어 작성
# /swapfile swap swap defaults 0 0

# # 파일의 맨 끝 다음줄에 아래 명령어 작성
# sudo echo "/swapfile swap swap defaults 0 0" >> /etc/fstab
echo "/swapfile swap swap defaults 0 0" | sudo tee -a /etc/fstab > /dev/null
