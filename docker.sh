##拉取基础镜像
#docker build -t chineseocr .
##启动服务
docker run -it --rm -p 8080:8080 chineseocr bash


