from flask_script import Manager
from interface import app, db
from flask_migrate import Migrate, MigrateCommand

#init
#migrate
#upgrade
#模型  -->迁移文件  ---> 表

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

# python sqlManage.py db init  :初始化一个迁移脚本的环境，只需要执行一次
# python sqlManage.py db migrate :将模型生成迁移文件，只要模型改变就需要执行
# python sqlManage.py db upgrade :把前一文件真正的映射到数据库中，每次运行了migrate就需要执行该命令
