��������rpc  
==
����:�����     

## �������:  
    ʹ��python3+��Windows����ʹ�ã������������õ�linux����
	���нڵ㶼��Ҫ��װpymysql��pikaģ�飻      
	����mysql��RabbitMQ���̳߳ص�ģ�鷽��ʵ�֣���������rpc��Զ�̹���    
	
## server��   
	�޸������ļ�     
		conf��setting.py
		�޸�mysql������Ϣ��RabbitMQ��ַ
	
	�������ļ�����mysql    
		1������mysql����һ����Ϊhost_manage�Ŀ�      
		CREATE DATABASE host_manage DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
		2��ʹ��host_manage��     
		use host_manage;       
		3�������ļ�     
		source ������ļ���;      
	
	ִ��������     
		ִ��bin��host_manage.py      
		�����û������루���ݿ����е�test\123 test2\123456��     
		    1.  ִ��shell����      
				�������û���������ַ;      
				����Ҫ�����������ַ���������Զ��ŷָ���     
				����shell������ؽ������ӡ��      
			2.  �鿴��������ַ      
				���ؽ������ӡ      
			3.  ���ӷ�������ַ      
				����ip��port��host_user��host_passwd��      
				����״̬����ӡ     
			4.  �޸ķ�������ַ     
				����Ҫ�޸ĵ�ip��     
				����Ҫ�޸ĵ�������     
				����Ҫ�޸ĵ�ֵ��     
				������Ӱ����������ӡ��     
			5.  ɾ����������ַ     
				����Ҫɾ����ip��    
				������Ӱ����������ӡ��     
			6.  �˳�     
				�˳���ǰ����      
				
## agent��  
	��rpc_agent.py����Զ�̿ͻ���
	ֻ��һ���ļ����༭�޸�RabbitMQ��ַ�ͱ�����ַ�����г���