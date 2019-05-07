service := requestbin
tag := red

main_image := registry:5000/jenkins/$(service):$(tag)
docker_build_args = \
	--build-arg GIT_COMMIT=$(shell git show -s --format=%H) \
	--build-arg GIT_COMMIT_DATE="$(shell git show -s --format=%ci)" \
	--build-arg IMAGE_NAME=$(service) \
	--build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%T.%N%Z") \
	--build-arg BUILD_URL=$(BUILD_URL) \
	--build-arg BUILD_NUMBER=$(BUILD_NUMBER)

# messaging-tertiary redis (via messaging-proxy), database 14
redis_url := //messaging-outbound.service.dev-central.consul:6381/14

.PHONY: build
build:
	docker build $(docker_build_args) --tag=$(main_image) .

.PHONY: push
push:
	docker push $(main_image)

.PHONY: run_drc
run_drc:
	docker run --rm -it --env REALM=prod --env REDIS_URL=$(redis_url) --publish-all $(main_image)
