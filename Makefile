# 发布 make release
.PHONY: release
release:
	python ./version-cli/auto_release.py

# 打包
# make build
.PHONY: build
build:
	python setup.py sdist bdist_wheel --python-tag py3

# 清空打包产物
clean:
	rm -rf temp logs .pytest_cache
	rm -rf dist build *.egg-info

# 上传打包产物到 pypi
upload:
	twine check dist/*
	twine upload dist/*

# 发布 make publish
publish:
	make clean
	make build
	make upload
	make clean


# 安装开发环境依赖
# make install-require
.PHONY: install-require
install-require:
	pip install -r requirements/development.txt

# 快速提交
# make fix
.PHONY: fix
fix:
	git add . && git commit -m 'fix' && git push

# 运行测试
# make test
.PHONY: test
test:
	python -m unittest tests/sqlite_database_test.py