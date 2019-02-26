#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <sys/types.h>
#include <sys/time.h>
int value=0;
//global variables
int round=0;
int finish_sign=0;
int num=0;
int remain_num=0;
int round_call=0;
//sem_t machine_sem;
int queue[20];//queue[0] represents num in queue;
int finish_guy[20];
sem_t finish_guy_lock;
sem_t all_finish;
sem_t queue_lock;//protect queue
pthread_t customer_thread[20];
pthread_t machine_thread[2];
struct machine_para{
	int G;
	int occupy;// 0 mean empty,1 mean occupy
	int accumulate_fail;
	int success[2];//0 for fail,1 for success
	int finish[2];//who finish, 0 for none
  sem_t G_lock;//protect accumulate_fail
	int just_start[2];//just start so don't accumulate fail
	int just_leave[2];
	int success_sign[2];
};
struct machine_para mp;

//

struct customer_para{
	int id;
	int arr;
	int conti;
	int rest;
	sem_t sem[2];
	sem_t machine_sem[2];
	int total;
	int conti_accum;
	int accumulate;
	int next_arr;
	int status;//0 for init,1 for wait,2 for clawing,3 for rest,4 for exit
  int on_machine;
	int wait_sign;
};





void *machine( void *ptr){


	struct customer_para *cp;
	cp=(struct customer_para*)ptr;
	//printf("Gakki:%d,%d,%d,%d,%d\n",(*cp).id,(*cp).arr,(*cp).conti,(*cp).rest,(*cp).total);
	while(1){

		int i=0;
    int machine_id=0;
    if(pthread_self()==machine_thread[0]){
      machine_id=1;
    }
    else if(pthread_self()==machine_thread[1]){
      machine_id=2;
    }
		//int value=0;
		//sem_getvalue(&cp[0].sem,&value);
		//printf("sem:%d\n",value);
    //sem_wait(&finish_guy_lock);

		for(i=0;i<num;i++){
			if(finish_guy[i]==0){
				sem_wait(&(cp[i].sem[machine_id-1]));
			}


		}
    //printf("round:%d\n",round);
    //printf("machine:%d\n",machine_id);
    //sem_post(&finish_guy_lock);
		//printf("queue\n");
	 	//for(i=0;i<num+1;i++){
		 	//printf("%d\n",queue[i+1]);
	 	//}
		//printf("machine round=%d\n\n",round);

		//printf("af:%d,%d\n\n",mp.accumulate_fail,mp.G);
		sem_wait(&mp.G_lock);


		//printf("round:%d\n",round);
		//printf("machine:%d\n",machine_id);

		if(mp.finish[machine_id-1]!=0){
			//printf("got it\n");
			if(mp.success[machine_id-1]==0){



				if(mp.accumulate_fail<mp.G){
					printf("%d %d finish playing NO #%d\n",round,mp.finish[machine_id-1],machine_id);
					cp[mp.finish[machine_id-1]-1].next_arr=round+cp[mp.finish[machine_id-1]-1].rest;
					cp[mp.finish[machine_id-1]-1].status=0;//claw to rest
					mp.just_leave[machine_id-1]=1;
					//mp.accumulate_fail++;
				}
				else{
					//printf("got it\n");
					printf("%d %d finish playing YES #%d\n",round,mp.finish[machine_id-1],machine_id);
					cp[mp.finish[machine_id-1]-1].status=4;//claw to exit
					pthread_cancel(customer_thread[mp.finish[machine_id-1]-1]);

					sem_post(&cp[mp.finish[machine_id-1]-1].sem[0]);
					sem_post(&cp[mp.finish[machine_id-1]-1].sem[1]);
					mp.success_sign[machine_id-1]=1;
					mp.accumulate_fail=0;
          //sem_wait(&finish_guy_lock);
					finish_guy[mp.finish[machine_id-1]-1]=1;
          //sem_post(&finish_guy_lock);
					remain_num--;


				}
		 }
     else if(mp.success[machine_id-1]==1){
				printf("%d %d finish playing YES #%d\n",round,mp.finish[machine_id-1],machine_id);
				//printf("got it\n");
				cp[mp.finish[machine_id-1]-1].status=4;//claw to exit
				pthread_cancel(customer_thread[mp.finish[machine_id-1]-1]);

				sem_post(&cp[mp.finish[machine_id-1]-1].sem[0]);
				sem_post(&cp[mp.finish[machine_id-1]-1].sem[1]);

				mp.success[machine_id-1]=0;
				mp.success_sign[machine_id-1]=1;
				mp.accumulate_fail=0;
        //sem_wait(&finish_guy_lock);
				finish_guy[mp.finish[machine_id-1]-1]=1;
        //sem_post(&finish_guy_lock);
				remain_num--;
		 }
		 mp.finish[machine_id-1]=0;
     sem_wait(&queue_lock);
		 //if()

     queue[machine_id]=queue[3];
		 for(i=3;i<num;i++){
				queue[i]=queue[i+1];
		 }

		 queue[0]--;

     sem_post(&queue_lock);
		 if(queue[0]==0){
				//mp.occupy=0;
				mp.accumulate_fail=0;
				//printf("empty queue\n");
		 }
		 if(queue[machine_id]!=0){

				cp[queue[machine_id]-1].status=2;
				printf("%d %d start playing #%d\n",round,queue[machine_id],machine_id);
				cp[queue[machine_id]-1].on_machine=machine_id;
				mp.just_start[machine_id-1]=1;
				cp[queue[machine_id]-1].wait_sign=0;
		 }
     //sem_post(&queue_lock);
		}
		else if(mp.accumulate_fail>=mp.G&&queue[machine_id]!=0){
			printf("%d %d finish playing YES #%d\n",round,queue[machine_id],machine_id);

			cp[queue[machine_id]-1].status=4;

			pthread_cancel(customer_thread[queue[machine_id]-1]);
			sem_post(&cp[queue[machine_id]-1].sem[0]);
			sem_post(&cp[queue[machine_id]-1].sem[1]);
			//printf("got it\n");
      //sem_wait(&finish_guy_lock);

			mp.success_sign[machine_id-1]=1;
			mp.accumulate_fail=0;
			finish_guy[queue[machine_id]-1]=1;
      //sem_post(&finish_guy_lock);
			remain_num--;
			//mp.finish[machine_id-1]=0;
			sem_wait(&queue_lock);
      queue[machine_id]=queue[3];
 		  for(i=3;i<num+1;i++){
 				queue[i]=queue[i+1];
 		  }
 		  queue[0]--;
			sem_post(&queue_lock);
			if(queue[machine_id]!=0){
				cp[queue[machine_id]-1].status=2;
				printf("%d %d start playing #%d\n",round,queue[machine_id],machine_id);
				mp.just_start[machine_id-1]=1;
				cp[queue[machine_id]-1].on_machine=machine_id;
				cp[queue[machine_id]-1].wait_sign=0;
			}



		}
		//sem_wait(&queue_lock);
		if((queue[machine_id]!=0&&mp.just_start[machine_id-1]==0)){
			//mp.accumulate_fail++;
			mp.just_leave[machine_id-1]=0;
		}

		//sem_post(&queue_lock);
		//printf("round:%d\n",round);
		//printf("queue\n");
		//for(i=0;i<num;i++){
			//printf("%d\n",queue[i+1]);
		//}
    //printf("machine:%d\n",machine_id);
		//printf("af:%d\n\n",mp.accumulate_fail);
		//printf("%d\n",queue[machine_id]);
    //printf("just_start:%d\n\n",mp.just_start[machine_id-1]);
    //printf("finish_guy:\n");

    //for(i=0;i<num;i++){

      //printf("%d:%d\n",i+1,finish_guy[i]);
    //}
		//if((mp.success_sign[0]+mp.success_sign[1])==1){
			//if(queue[1]||queue[2]){
				//mp.accumulate_fail++;
			//}
			//mp.success_sign[0]=0;
		//}

    sem_post(&mp.G_lock);
    //int value;
    //sem_getvalue(&queue_lock,&value);
    //printf("machine:%d,queue_lock:%d\n",machine_id,value);
		/*for(i=0;i<remain_num;i++){
			sem_post(&machine_sem);
		}*/
		//printf("round:%d\n",round);
		//printf("machine:%d\n",machine_id);
    round_call++;
    if(round_call==2){
      round++;
      round_call=0;
    }
    //int value=0;
    //sem_getvalue(&finish_guy_lock,&value);
    //printf("finish_guy_lock:%d\n",value);
		for(i=0;i<num;i++){
      //sem_wait(&finish_guy_lock);
			if(finish_guy[i]==0){
				sem_post(&(cp[i].machine_sem[machine_id-1]));
			}
      //sem_post(&finish_guy_lock);
      int value=0;
      //sem_getvalue(&cp[i].sem[1],&value);
      //printf("sem:%d\n",value);
		if(remain_num==0){
			//printf("%d\n",cp[mp.finish-1].status);
			//printf("Machine exit\n");
			//int value;
			//sem_post(&machine_sem);
			//sem_getvalue(&machine_sem, &value);
			//printf("%d\n",value);
			sem_post(&all_finish);
			pthread_exit(NULL);
		}

	}
  //printf("end\n");

}

}
void *customer(void *ptr){

	struct customer_para *cp;

	cp=(struct customer_para*)ptr;


	int id=(*cp).id;
	int index=id-1;
	cp-=index;
	//printf("")
	while(1){
		//printf("Gakki:%d,%d,%d,%d,%d\n",(*cp).id,(*cp).arr,(*cp).conti,(*cp).rest,(*cp).total);
		//round++;
		//if(round==30)pthread_exit(NULL);
		sem_wait(&(cp[index].machine_sem[0]));
    sem_wait(&(cp[index].machine_sem[1]));
		//printf("customer round=%d\n",round);
		//printf("customer id=%d\n",id);
		//printf("customer %d,%d,%d,%d,%d\n",id,cp[index].arr,cp[index].conti,cp[index].rest,cp[index].total);
		//int value=0;
		//sem_getvalue(&cp[index].machine_sem,&value);
		//printf("machine_sem:%d\n",value);
		int i=0;
		if(cp[index].wait_sign==1){
			printf("%d %d wait in line\n",round-1,id);
			cp[index].wait_sign=0;
		}
		//printf("round:%d\n",round);
		//printf("id:%d\n",id);
		//printf("status:%d\n",cp[index].status);
		//printf("on_machine:%d\n\n",cp[index].on_machine);

		//printf("status:%d\n\n",cp[index].status);
		if(cp[index].status==0){

			if(round==cp[index].next_arr){
        sem_wait(&queue_lock);
				if(queue[0]==0||queue[0]==1){
          if(queue[1]==0){
            printf("%d %d start playing #1\n",round,id);
						//printf("got it\n");
						mp.just_start[0]=1;
  					queue[0]++;
  					queue[1]=id;
            cp[index].on_machine=1;
  					cp[index].status=2;//rest to claw
          }
          else if(queue[2]==0){
            printf("%d %d start playing #2\n",round,id);
            //sem_wait(&queue_lock);
						mp.just_start[1]=1;
  					queue[0]++;
  					queue[2]=id;
            cp[index].on_machine=2;
  					cp[index].status=2;//rest to claw
          }

				}

				//wait
				else{
					//printf("%d %d wait in line\n",round,id);
          //sem_wait(&queue_lock);
					cp[index].wait_sign=1;
					queue[queue[0]+1]=id;
					queue[0]++;
					cp[index].status=1;//rest to wait
				}
        sem_post(&queue_lock);
			}
		}
		else if(cp[index].status==2){

			cp[index].accumulate++;
			cp[index].conti_accum++;
			mp.accumulate_fail++;
      //printf("id:%d\n",id);
      //printf("round:%d\n",round);
			//printf("conti:%d,%d\n",cp[index].conti_accum,cp[index].conti);
			mp.just_start[cp[index].on_machine-1]=0;
			if(cp[index].accumulate==cp[index].total){
				/*printf("%d %d finish playing YES",round,id);
				for(i=1;i<queue[0];i++){
					queue[i]=queue[i+1];
				}
				queue[0]--;*/
				//mp.accumulate_fail=0;

				mp.finish[cp[index].on_machine-1]=id;
				mp.success[cp[index].on_machine-1]=1;

				//num--;
				//pthread_exit(NULL);
			}
			else if(cp[index].conti_accum==cp[index].conti){

				mp.finish[cp[index].on_machine-1]=id;
				cp[index].conti_accum=0;
				//printf("IIII:%d\n",mp.finish);
				mp.success[cp[index].on_machine-1]=0;
				//cp[index].status==3;//claw finish to rest
			}
		}
  	/*else if(cp[index].status==3){
			if(round==cp[index].next_arr){
        sem_wait(&queue_lock);
				if(queue[0]==0||queue[0]==1){
          if(queue[1]==0){
            printf("%d %d start playing #1\n",round,id);

  					queue[0]++;
  					queue[1]=id;
  					cp[index].status=2;//rest to claw
          }
          else if(queue[2]==0){
            printf("%d %d start playing #2\n",round,id);
            //sem_wait(&queue_lock);
  					queue[0]++;
  					queue[2]=id;
  					cp[index].status=2;//rest to claw
          }

				}

				//wait
				else{
					printf("%d %d wait in line\n",round,id);
          //sem_wait(&queue_lock);
					queue[queue[0]+1]=id;
					queue[0]++;
					cp[index].status=1;//rest to wait
				}
        sem_post(&queue_lock);
			}
		}*/
		sem_post(&(cp[index].sem[0]));
    sem_post(&(cp[index].sem[1]));
		/*else if(cp[index].status==4){
			printf("customer %d out\n",id);
			pthread_exit(NULL);
		}*/
		/*if(cp[index].status==4){
			printf("customer %d out\n",id);

			if(remain_num==0){

				sem_post(&all_finish);
			}
			//sem_post(&(cp[index].sem));
			pthread_exit(NULL);
		}*/








	}




}



int main(int argc,char *argv[]){


	struct customer_para cp[20];


	char file[100];
  int i=0;
	//file=argv[1];
	mp.occupy=0;
	mp.accumulate_fail=0;
  for(i=0;i<2;i++){
    mp.success[i]=0;
  	mp.finish[i]=0;
		mp.just_start[i]=0;
		mp.just_leave[i]=0;
		mp.success_sign[i]=0;
  }

	//printf("enter file name:");
	//scanf("%s",file);
	FILE *fp,*out1,*out2;
	fp=fopen(argv[1],"r");
  sem_init(&queue_lock,1,1);
  sem_init(&finish_guy_lock,1,1);
	sem_init(&all_finish,1,0);
  sem_init(&mp.G_lock,1,1);
  int var=0;

	fscanf(fp,"%d",&(mp.G));
	fscanf(fp,"%d",&num);
	remain_num=num;
	//sem_init(&machine_sem,1,num);
	for(i=0;i<num;i++){
		cp[i].id=i+1;
		fscanf(fp,"%d",&var);
		cp[i].arr=var;
		cp[i].next_arr=var;
		fscanf(fp,"%d",&var);
		cp[i].conti=var;
		fscanf(fp,"%d",&var);
		cp[i].rest=var;
		fscanf(fp,"%d",&var);
		cp[i].total=var;
		sem_init(&(cp[i].sem[0]),1,0);
    sem_init(&(cp[i].sem[1]),1,0);
		sem_init(&(cp[i].machine_sem[0]),1,1);
    sem_init(&(cp[i].machine_sem[1]),1,1);
		cp[i].accumulate=0;
		cp[i].status=0;
		cp[i].conti_accum=0;
		cp[i].on_machine=0;
		cp[i].wait_sign=0;
	}
	fclose(fp);
	/*for(i=0;i<num;i++){
		printf("%d\n",cp[i].id);
	}*/
	for(i=0;i<num;i++){
		//printf("%d\n",cp[i].id);
		pthread_create(customer_thread+i,NULL,customer,(void*)(cp+i));
		//printf("Gakki");
	}
  for(i=0;i<2;i++){

  }
	pthread_create(machine_thread,NULL,machine,(void*)cp);
  pthread_create(machine_thread+1,NULL,machine,(void*)cp);
	//printf("Gakki");

	//pthread_join(&machine_thread,NULL);
	sem_wait(&all_finish);
	//printf("end\n");
	//for(i=0;i<num;i++){
	//	pthread_join(customer_thread+i,NULL);
	//}


	//printf("end\n");
   return 0;
}
