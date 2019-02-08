#http://archive.4plebs.org/_/api/chan/thread/?board=adv&num=16627902
#http://archive.4plebs.org/_/api/chan/index/?board=adv&page=1
import json
import threading
import requests
import time as time
def helper(board,k,j):
    allPage=[]
    file=open('4pleb'+'_'+board+'_'+str(k)+'_json','w')
    q=0
    i=k
    error=open(board+'.error','w')
    while(1):
        q=q+1
        if q%10==0:
            print(i)
        for x in range(0,2):
            
            while True:
                try:
                    r=requests.get("http://archive.4plebs.org/_/api/chan/index/?board="+board+"&page="+str(i+x))
                    break
                except:
                    print("Wait")
                    time.sleep(60)
            if len(r.content)>5:
                
                try:
                    page=r.json()
                    for p in page:
                        
                        file.write(p+'\n')
                except:
                    error.write(str(i)+','+board+'\n')
                
            else:
                
                break
        
        i=int(q)*int(j)+int(k)
        
        
    file.close()    


t0 = threading.Thread(target=helper,args=("pol",100,100)) 
t0.daemon =True
t0.start()

t1 = threading.Thread(target=helper,args=("pol",1,100)) 
t1.daemon =True
t1.start()

t2 = threading.Thread(target=helper,args=("pol",2,100)) 
t2.daemon =True
t2.start()

t3 = threading.Thread(target=helper,args=("pol",3,100)) 
t3.daemon =True
t3.start()

t4 = threading.Thread(target=helper,args=("pol",4,100)) 
t4.daemon =True
t4.start()

t5 = threading.Thread(target=helper,args=("pol",5,100)) 
t5.daemon =True
t5.start()

t6 = threading.Thread(target=helper,args=("pol",6,100)) 
t6.daemon =True
t6.start()

t7 = threading.Thread(target=helper,args=("pol",7,100)) 
t7.daemon =True
t7.start()

t8 = threading.Thread(target=helper,args=("pol",8,100)) 
t8.daemon =True
t8.start()

t9 = threading.Thread(target=helper,args=("pol",9,100)) 
t9.daemon =True
t9.start()

t10 = threading.Thread(target=helper,args=("pol",10,100)) 
t10.daemon =True
t10.start()

t11 = threading.Thread(target=helper,args=("pol",11,100)) 
t11.daemon =True
t11.start()

t12 = threading.Thread(target=helper,args=("pol",12,100)) 
t12.daemon =True
t12.start()

t13 = threading.Thread(target=helper,args=("pol",13,100)) 
t13.daemon =True
t13.start()

t14 = threading.Thread(target=helper,args=("pol",14,100)) 
t14.daemon =True
t14.start()

t15 = threading.Thread(target=helper,args=("pol",15,100)) 
t15.daemon =True
t15.start()

t16 = threading.Thread(target=helper,args=("pol",16,100)) 
t16.daemon =True
t16.start()

t17 = threading.Thread(target=helper,args=("pol",17,100)) 
t17.daemon =True
t17.start()

t18 = threading.Thread(target=helper,args=("pol",18,100)) 
t18.daemon =True
t18.start()

t19 = threading.Thread(target=helper,args=("pol",19,100)) 
t19.daemon =True
t19.start()

t20 = threading.Thread(target=helper,args=("pol",20,100)) 
t20.daemon =True
t20.start()

t21 = threading.Thread(target=helper,args=("pol",21,100)) 
t21.daemon =True
t21.start()

t22 = threading.Thread(target=helper,args=("pol",22,100)) 
t22.daemon =True
t22.start()

t23 = threading.Thread(target=helper,args=("pol",23,100)) 
t23.daemon =True
t23.start()

t24 = threading.Thread(target=helper,args=("pol",24,100)) 
t24.daemon =True
t24.start()

t25 = threading.Thread(target=helper,args=("pol",25,100)) 
t25.daemon =True
t25.start()

t26 = threading.Thread(target=helper,args=("pol",26,100)) 
t26.daemon =True
t26.start()

t27 = threading.Thread(target=helper,args=("pol",27,100)) 
t27.daemon =True
t27.start()

t28 = threading.Thread(target=helper,args=("pol",28,100)) 
t28.daemon =True
t28.start()

t29 = threading.Thread(target=helper,args=("pol",29,100)) 
t29.daemon =True
t29.start()

t30 = threading.Thread(target=helper,args=("pol",30,100)) 
t30.daemon =True
t30.start()

t31 = threading.Thread(target=helper,args=("pol",31,100)) 
t31.daemon =True
t31.start()

t32 = threading.Thread(target=helper,args=("pol",32,100)) 
t32.daemon =True
t32.start()

t33 = threading.Thread(target=helper,args=("pol",33,100)) 
t33.daemon =True
t33.start()

t34 = threading.Thread(target=helper,args=("pol",34,100)) 
t34.daemon =True
t34.start()

t35 = threading.Thread(target=helper,args=("pol",35,100)) 
t35.daemon =True
t35.start()

t36 = threading.Thread(target=helper,args=("pol",36,100)) 
t36.daemon =True
t36.start()

t37 = threading.Thread(target=helper,args=("pol",37,100)) 
t37.daemon =True
t37.start()

t38 = threading.Thread(target=helper,args=("pol",38,100)) 
t38.daemon =True
t38.start()

t39 = threading.Thread(target=helper,args=("pol",39,100)) 
t39.daemon =True
t39.start()

t40 = threading.Thread(target=helper,args=("pol",40,100)) 
t40.daemon =True
t40.start()

t41 = threading.Thread(target=helper,args=("pol",41,100)) 
t41.daemon =True
t41.start()

t42 = threading.Thread(target=helper,args=("pol",42,100)) 
t42.daemon =True
t42.start()

t43 = threading.Thread(target=helper,args=("pol",43,100)) 
t43.daemon =True
t43.start()

t44 = threading.Thread(target=helper,args=("pol",44,100)) 
t44.daemon =True
t44.start()

t45 = threading.Thread(target=helper,args=("pol",45,100)) 
t45.daemon =True
t45.start()

t46 = threading.Thread(target=helper,args=("pol",46,100)) 
t46.daemon =True
t46.start()

t47 = threading.Thread(target=helper,args=("pol",47,100)) 
t47.daemon =True
t47.start()

t48 = threading.Thread(target=helper,args=("pol",48,100)) 
t48.daemon =True
t48.start()

t49 = threading.Thread(target=helper,args=("pol",49,100)) 
t49.daemon =True
t49.start()

t50 = threading.Thread(target=helper,args=("pol",50,100)) 
t50.daemon =True
t50.start()

t51 = threading.Thread(target=helper,args=("pol",51,100)) 
t51.daemon =True
t51.start()

t52 = threading.Thread(target=helper,args=("pol",52,100)) 
t52.daemon =True
t52.start()

t53 = threading.Thread(target=helper,args=("pol",53,100)) 
t53.daemon =True
t53.start()

t54 = threading.Thread(target=helper,args=("pol",54,100)) 
t54.daemon =True
t54.start()

t55 = threading.Thread(target=helper,args=("pol",55,100)) 
t55.daemon =True
t55.start()

t56 = threading.Thread(target=helper,args=("pol",56,100)) 
t56.daemon =True
t56.start()

t57 = threading.Thread(target=helper,args=("pol",57,100)) 
t57.daemon =True
t57.start()

t58 = threading.Thread(target=helper,args=("pol",58,100)) 
t58.daemon =True
t58.start()

t59 = threading.Thread(target=helper,args=("pol",59,100)) 
t59.daemon =True
t59.start()

t60 = threading.Thread(target=helper,args=("pol",60,100)) 
t60.daemon =True
t60.start()

t61 = threading.Thread(target=helper,args=("pol",61,100)) 
t61.daemon =True
t61.start()

t62 = threading.Thread(target=helper,args=("pol",62,100)) 
t62.daemon =True
t62.start()

t63 = threading.Thread(target=helper,args=("pol",63,100)) 
t63.daemon =True
t63.start()

t64 = threading.Thread(target=helper,args=("pol",64,100)) 
t64.daemon =True
t64.start()

t65 = threading.Thread(target=helper,args=("pol",65,100)) 
t65.daemon =True
t65.start()

t66 = threading.Thread(target=helper,args=("pol",66,100)) 
t66.daemon =True
t66.start()

t67 = threading.Thread(target=helper,args=("pol",67,100)) 
t67.daemon =True
t67.start()

t68 = threading.Thread(target=helper,args=("pol",68,100)) 
t68.daemon =True
t68.start()

t69 = threading.Thread(target=helper,args=("pol",69,100)) 
t69.daemon =True
t69.start()

t70 = threading.Thread(target=helper,args=("pol",70,100)) 
t70.daemon =True
t70.start()

t71 = threading.Thread(target=helper,args=("pol",71,100)) 
t71.daemon =True
t71.start()

t72 = threading.Thread(target=helper,args=("pol",72,100)) 
t72.daemon =True
t72.start()

t73 = threading.Thread(target=helper,args=("pol",73,100)) 
t73.daemon =True
t73.start()

t74 = threading.Thread(target=helper,args=("pol",74,100)) 
t74.daemon =True
t74.start()

t75 = threading.Thread(target=helper,args=("pol",75,100)) 
t75.daemon =True
t75.start()

t76 = threading.Thread(target=helper,args=("pol",76,100)) 
t76.daemon =True
t76.start()

t77 = threading.Thread(target=helper,args=("pol",77,100)) 
t77.daemon =True
t77.start()

t78 = threading.Thread(target=helper,args=("pol",78,100)) 
t78.daemon =True
t78.start()

t79 = threading.Thread(target=helper,args=("pol",79,100)) 
t79.daemon =True
t79.start()

t80 = threading.Thread(target=helper,args=("pol",80,100)) 
t80.daemon =True
t80.start()

t81 = threading.Thread(target=helper,args=("pol",81,100)) 
t81.daemon =True
t81.start()

t82 = threading.Thread(target=helper,args=("pol",82,100)) 
t82.daemon =True
t82.start()

t83 = threading.Thread(target=helper,args=("pol",83,100)) 
t83.daemon =True
t83.start()

t84 = threading.Thread(target=helper,args=("pol",84,100)) 
t84.daemon =True
t84.start()

t85 = threading.Thread(target=helper,args=("pol",85,100)) 
t85.daemon =True
t85.start()

t86 = threading.Thread(target=helper,args=("pol",86,100)) 
t86.daemon =True
t86.start()

t87 = threading.Thread(target=helper,args=("pol",87,100)) 
t87.daemon =True
t87.start()

t88 = threading.Thread(target=helper,args=("pol",88,100)) 
t88.daemon =True
t88.start()

t89 = threading.Thread(target=helper,args=("pol",89,100)) 
t89.daemon =True
t89.start()

t90 = threading.Thread(target=helper,args=("pol",90,100)) 
t90.daemon =True
t90.start()

t91 = threading.Thread(target=helper,args=("pol",91,100)) 
t91.daemon =True
t91.start()

t92 = threading.Thread(target=helper,args=("pol",92,100)) 
t92.daemon =True
t92.start()

t93 = threading.Thread(target=helper,args=("pol",93,100)) 
t93.daemon =True
t93.start()

t94 = threading.Thread(target=helper,args=("pol",94,100)) 
t94.daemon =True
t94.start()

t95 = threading.Thread(target=helper,args=("pol",95,100)) 
t95.daemon =True
t95.start()

t96 = threading.Thread(target=helper,args=("pol",96,100)) 
t96.daemon =True
t96.start()

t97 = threading.Thread(target=helper,args=("pol",97,100)) 
t97.daemon =True
t97.start()

t98 = threading.Thread(target=helper,args=("pol",98,100)) 
t98.daemon =True
t98.start()

t99 = threading.Thread(target=helper,args=("pol",99,100)) 
t99.daemon =True
t99.start()

a=t0.join()
a=t1.join()
a=t2.join()
a=t3.join()
a=t4.join()
a=t5.join()
a=t6.join()
a=t7.join()
a=t8.join()
a=t9.join()
a=t10.join()
a=t11.join()
a=t12.join()
a=t13.join()
a=t14.join()
a=t15.join()
a=t16.join()
a=t17.join()
a=t18.join()
a=t19.join()
a=t20.join()
a=t21.join()
a=t22.join()
a=t23.join()
a=t24.join()
a=t25.join()
a=t26.join()
a=t27.join()
a=t28.join()
a=t29.join()
a=t30.join()
a=t31.join()
a=t32.join()
a=t33.join()
a=t34.join()
a=t35.join()
a=t36.join()
a=t37.join()
a=t38.join()
a=t39.join()
a=t40.join()
a=t41.join()
a=t42.join()
a=t43.join()
a=t44.join()
a=t45.join()
a=t46.join()
a=t47.join()
a=t48.join()
a=t49.join()
a=t50.join()
a=t51.join()
a=t52.join()
a=t53.join()
a=t54.join()
a=t55.join()
a=t56.join()
a=t57.join()
a=t58.join()
a=t59.join()
a=t60.join()
a=t61.join()
a=t62.join()
a=t63.join()
a=t64.join()
a=t65.join()
a=t66.join()
a=t67.join()
a=t68.join()
a=t69.join()
a=t70.join()
a=t71.join()
a=t72.join()
a=t73.join()
a=t74.join()
a=t75.join()
a=t76.join()
a=t77.join()
a=t78.join()
a=t79.join()
a=t80.join()
a=t81.join()
a=t82.join()
a=t83.join()
a=t84.join()
a=t85.join()
a=t86.join()
a=t87.join()
a=t88.join()
a=t89.join()
a=t90.join()
a=t91.join()
a=t92.join()
a=t93.join()
a=t94.join()
a=t95.join()
a=t96.join()
a=t97.join()
a=t98.join()
a=t99.join()

