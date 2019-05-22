#!/usr/bin/env python3
from flask import Flask, render_template, request, json, jsonify
from time import sleep
from multiprocessing import Value
import threading
import requests
import docker 


first_flag=0


def autoscale():
	global no_of_containers
	with count.get_lock():
		containers_to_run=int(count.value/20)+1
		
		containers_to_start=containers_to_run-no_of_containers
		print("containers to start ",containers_to_start)
		if(containers_to_start<0):#reducing the containers
			doc_obj2=docker.from_env()
			container_list2=doc_obj2.containers.list()
			container_flag=-(containers_to_start)
			container_delete_list=[]
			temp=no_of_containers
			while(container_flag!=0):
				container_delete_list.append(int(8000+temp-1))
				print("added to delete list",8000+temp-1)
				temp=temp-1
				container_flag=container_flag-1
			for a1 in container_list2:
				try:
					print("container:",a1)
					p=a1.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
					print("port :" ,p)
					print("Number of containers",no_of_containers)
					print("port number to delete", 8000+no_of_containers-1)
					print("truth of p",int(p)==int( 8000 + no_of_containers-1))
					if int(p) in container_delete_list:
						print("container deleted at port :",int(p))
						a1.kill()
						no_of_containers=no_of_containers-1
						
				except:
					pass
			
		elif containers_to_start>0:#increasing the containers
			for i in range(containers_to_start):
				doc_obj1=docker.from_env()
				print("container start ")
				doc_obj1.containers.run(image='acts',detach=True,volumes={'acts': {'bind': '/app/some','mode': 'rw'}},ports={'80/tcp':8000+(no_of_containers)})
				print(8000+no_of_containers)
				no_of_containers=no_of_containers+1
		count.value=0		


def autoscale_thread():
	print("scaling under work")
	while True:
		sleep(120)
		autoscale()
		
t2=threading.Thread(target=autoscale_thread)

				
app=Flask(__name__)


count=Value('i',0)
no_of_containers=1

@app.route("/api/v1/_health", methods=['GET'])
def health():
	with count.get_lock():
		#count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get('http://localhost:'+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype='application/json')
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response
@app.route("/api/v1/_crash",methods=['POST'])
def crash():
	with count.get_lock():
		#count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
		response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response

@app.route("/api/v1/_count", methods=['GET'])
def get_count():
	with count.get_lock():
		#count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get('http://localhost:'+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype='application/json')
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response
@app.route("/api/v1/_count", methods=['DELETE'])
def delete_count():
	with count.get_lock():
		#count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.delete("http://localhost:"+str(8000+port)+str(request.full_path))
		return json.dumps({}),mid_response.status_code



@app.route('/api/v1/categories', methods = ['GET'])
def get_categories():
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
	with count.get_lock():
		count.value=count.value+1
		
		port=count.value%no_of_containers
		mid_response=requests.get('http://localhost:'+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype='application/json')
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response

@app.route('/api/v1/categories', methods = ['POST'])
def post_categories():
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
		response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response


@app.route('/api/v1/categories/<categoryName>', methods = ['DELETE'])
def delete_categories(categoryName):
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.delete("http://localhost:"+str(8000+port)+str(request.full_path))
		return json.dumps({}),mid_response.status_code

@app.route('/api/v1/categories/<categoryName>/acts', methods = ['GET'])
def get_catefories_acts(categoryName):
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get("http://localhost:"+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype="application/json")
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype="application/json")
		return response
@app.route('/api/v1/categories/<categoryName>/acts/size', methods = ['GET'])
def get_catefories_acts_count(categoryName):
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass

	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get("http://localhost:"+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype="application/json")
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype="application/json")
		return response


@app.route('/api/v1/categories/<categoryName>/acts?start=<startRange>&end=<endRange>', methods = ['GET'])
def get_catefories_acts_count_100(categoryName,startRange,endRange):
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get("http://localhost:"+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype="application/json")
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype="application/json")
		return response

@app.route('/api/v1/acts/upvote', methods = ['POST'])
def upvote_act():
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass
	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
		response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response


@app.route('/api/v1/acts/<actid>', methods = ['DELETE'])
def delete_acts(actid):
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass

	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.delete("http://localhost:"+str(8000+port)+str(request.full_path))
		return json.dumps({}),mid_response.status_code

@app.route('/api/v1/acts', methods = ['POST'])
def post_acts():
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass

	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.post(url="http://localhost:"+str(8000+port)+str(request.full_path),json=request.get_json())
		response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response

@app.route('/api/v1/acts/count',methods=['GET'])
def get_acts_count():
	global first_flag
	if count.value==0 and first_flag==0:
		try:
			t2.start()
			first_flag=1
		except:
			pass

	with count.get_lock():
		count.value=count.value+1
		port=count.value%no_of_containers
		mid_response=requests.get('http://localhost:'+str(8000+port)+str(request.full_path))
		try:
			data=mid_response.json()
			response=app.response_class(response=json.dumps(data),status=mid_response.status_code,mimetype='application/json')
		except:
			response=app.response_class(response=json.dumps({}),status=mid_response.status_code,mimetype='application/json')
		return response






def fault_tolerence():
	
	doc_obj=docker.from_env()
	container_list=doc_obj.containers.list()	
	container_count=0
	global no_of_containers
	with count.get_lock():
		for a in container_list:
			if(container_count<no_of_containers):
				#print("in loop")
				try:
					p=a.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
					r=requests.get('http://localhost:'+str(p)+"/api/v1/_health")
					if r.status_code!=200:
						print("killing the container ",p)
						a.kill()
						doc_obj.containers.run(image='acts',detach=True,volumes={'acts': {'bind': '/app/some','mode': 'rw'}},ports={'80/tcp':p})
					container_count=container_count+1
				except:
					pass

def fault_tolerence_thread():
	print("fault tolerence thread started")
	while True:
		fault_tolerence()
		sleep(1)
		




t1=threading.Thread(target=fault_tolerence_thread)

t1.start()
app.run(host='0.0.0.0',port='80',debug=True)
