# 创建数据库表
```shell
# 创建数据库
(env) $ flask shell
>>> from app import db
>>> db.create_all()

# 如果你改动了模型类，想重新生成表模式，那么需要先使用 db.drop_all() 删除表，然后重新创建：
# 注意这会一并删除所有数据，如果你想在不破坏数据库内的数据的前提下变更表的结构，需要使用数据库迁移工具，比如集成了 Alembic 的 Flask-Migrate 扩展。
>>> db.drop_all()
>>> db.create_all()
```

# 单元测试
```shell
#coverage run --source=app test_watchlist.py
coverage run --source=watchlist test_watchlist.py
```
# 生成依赖文件
```shell
 pip freeze > requirements.txt
```

# 启动
```shell
flask run
或
uwsgi --ini uwsgi.ini
或
uwsgi --http :8001 --wsgi-file wsgi.py --virtualenv ~/.virtualenvs/flaskProject
```