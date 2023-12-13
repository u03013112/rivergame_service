TAG=v1
ACCOUNT=u03013112
FEISHU_IMAGE=${ACCOUNT}/feishu:${TAG}

all:
	docker build -f docker/feishu.dockerfile -t ${FEISHU_IMAGE} .
push:
	docker push ${FEISHU_IMAGE} 