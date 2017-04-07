主机管理rpc  
==
作者:王宇夫     

## 程序介绍:  
    使用python3+、Windows环境使用，主机服务器用的linux；、
	所有节点都需要安装pymysql、pika模块；      
	利用mysql、RabbitMQ、线程池的模块方法实现，主机基于rpc的远程管理。    
	
## server：   
	修改配置文件     
		conf下setting.py
		修改mysql连接信息和RabbitMQ地址
	
	将备份文件导入mysql    
		1、进入mysql创建一个名为host_manage的库      
		CREATE DATABASE host_manage DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
		2、使用host_manage库     
		use host_manage;       
		3、导入文件     
		source 导入的文件名;      
	
	执行主程序     
		执行bin下host_manage.py      
		输入用户名密码（数据库中有的test\123 test2\123456）     
		    1.  执行shell命令      
				看到此用户的主机地址;      
				输入要管理的主机地址，输入多个以逗号分隔；     
				输入shell命令，返回结果，打印。      
			2.  查看服务器地址      
				返回结果，打印      
			3.  增加服务器地址      
				输入ip、port、host_user、host_passwd；      
				返回状态并打印     
			4.  修改服务器地址     
				输入要修改的ip；     
				输入要修改的列名；     
				输入要修改的值；     
				返回收影响行数，打印。     
			5.  删除服务器地址     
				输入要删除的ip；    
				返回收影响行数，打印。     
			6.  退出     
				退出当前程序      
				
## agent：  
	将rpc_agent.py部署到远程客户端
	只有一个文件，编辑修改RabbitMQ地址和本机地址，运行程序