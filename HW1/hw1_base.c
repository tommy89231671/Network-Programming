#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <sys/types.h>
#include <sys/time.h>

//global variables
int round=0;
int num=0;
int remain_num=0;
//sem_t machine_sem;
int queue[20];//queue[0] represents num in queue;
int finish_guy[20];
sem_t all_finish;
pthread_t customer_thread[20];
pthread_t machine_thread;

struct machine_para{
	int G;
	int occupy;// 0 mean empty,1 mean occupy
	int accumulate_fail;
	int success;//0 for fail,1 for success
	int finish;//who finish, 0 for none
};
struct machine_para mp;

//

struct customer_para{
	int id;
	int arr;
	int conti;
	int rest;
	sem_t sem;
	sem_t machine_sem;
	int total;
	int conti_accum;
	int accumulate;
	int next_arr;
	int status;//0 for init,1 for wait,2 for clawing,3 for rest,4 for exit
	int wait_sign;
};





void *machine( void *ptr){

	struct customer_para *cp;
	cp=(struct customer_para*)ptr;
	//printf("Gakki:%d,%d,%d,%d,%d\n",(*cp).id,(*cp).arr,(*cp).conti,(*cp).rest,(*cp).total);
	while(1){

		int i=0;
		///problem to solve
		int value=0;
		sem_getvalue(&cp[0].sem,&value);
		//printf("sem:%d\n",value);
		for(i=0;i<num;i++){
			if(finish_guy[i]==0){
				sem_wait(&(cp[i].sem));
			}


		}
		//printf("machine round=%d\n\n",round);

		//printf("af:%d,%d\n",mp.accumulate_fail,mp.G);



		if(mp.finish!=0){
			//printf("got it\n");
			if(mp.success==0){



				if(mp.accumulate_fail!=mp.G){
					printf("%d %d finish playing NO\n",round,mp.finish);
					cp[mp.finish-1].next_arr=round+cp[mp.finish-1].rest;
					cp[mp.finish-1].status=0;//claw to rest
				}
				else{
				//	printf("got it\n");
					printf("%d %d finish playing YES\n",round,mp.finish);
					cp[mp.finish-1].status=4;//claw to exit
					pthread_cancel(customer_thread[mp.finish-1]);
					mp.accumulate_fail=0;
					finish_guy[mp.finish-1]=1;
					remain_num--;


				}
			}
			else if(mp.success==1){
				printf("%d %d finish playing YES\n",round,mp.finish);
				//printf("got it\n");
				//cp[mp.finish-1].status=4;//claw to exit
				pthread_cancel(customer_thread[mp.finish-1]);
				mp.success=0;
				mp.accumulate_fail=0;
				finish_guy[mp.finish-1]=1;
				remain_num--;
			}
			mp.finish=0;
			for(i=1;i<queue[0];i++){
				queue[i]=queue[i+1];
			}
			queue[0]--;
			if(queue[0]==0){
				mp.occupy=0;
				mp.accumulate_fail=0;
				//printf("empty queue\n");
			}
			if(queue[0]!=0){

				cp[queue[1]-1].status=2;
				printf("%d %d start playing\n",round,queue[1]);
				cp[queue[1]-1].wait_sign=0;
			}

		}
		else if(mp.accumulate_fail==mp.G){
			printf("%d %d finish playing YES\n",round,queue[1]);
			pthread_cancel(customer_thread[queue[1]-1]);
			cp[queue[1]-1].status=4;
			mp.accumulate_fail=0;
			finish_guy[queue[1]-1]=1;
			remain_num--;
			mp.finish=0;
			for(i=1;i<queue[0];i++){
				queue[i]=queue[i+1];
			}
			queue[0]--;
			if(queue[0]!=0){
				cp[queue[1]-1].status=2;
				printf("%d %d start playing\n",round,queue[1]);
				cp[queue[1]-1].wait_sign=0;
			}
		}
		if(queue[0]!=0){
			mp.accumulate_fail++;

		}


		/*for(i=0;i<remain_num;i++){
			sem_post(&machine_sem);
		}*/
		round++;
		for(i=0;i<num;i++){
			if(finish_guy[i]==0){
				sem_post(&(cp[i].machine_sem));
			}
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

		//if(round==30)pthread_exit(NULL);

	}


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
		sem_wait(&(cp[index].machine_sem));
		//printf("customer round=%d\n",round);
		//printf("customer id=%d\n",id);
		//printf("customer %d,%d,%d,%d,%d\n",id,cp[index].arr,cp[index].conti,cp[index].rest,cp[index].total);
		//int value=0;
		//sem_getvalue(&cp[index].machine_sem,&value);
		//printf("machine_sem:%d\n",value);
		if(cp[index].wait_sign==1){
			printf("%d %d wait in line\n",round-1,id);
			cp[index].wait_sign=0;
		}

		int i=0;
		//printf("status:%d\n\n",cp[index].status);
		if(cp[index].status==0){

			if(round==cp[index].next_arr){
				if(queue[0]==0){
					printf("%d %d start playing\n",round,id);
					queue[0]++;
					queue[1]=id;
					cp[index].status=2;
				}
				//wait
				else{
					//printf("%d %d wait in line\n",round,id);
					cp[index].wait_sign=1;
					queue[queue[0]+1]=id;
					queue[0]++;
					cp[index].status=1;
				}
			}
		}
		else if(cp[index].status==2){

			cp[index].accumulate++;
			cp[index].conti_accum++;
			//printf("round:%d",round);
			//printf("conti:%d,%d\n",cp[index].conti_accum,cp[index].conti);
			if(cp[index].accumulate==cp[index].total){
				/*printf("%d %d finish playing YES",round,id);
				for(i=1;i<queue[0];i++){
					queue[i]=queue[i+1];
				}
				queue[0]--;*/
				//mp.accumulate_fail=0;
				mp.finish=id;
				mp.success=1;

				//num--;
				//pthread_exit(NULL);
			}
			else if(cp[index].conti_accum==cp[index].conti){
				mp.finish=id;
				cp[index].conti_accum=0;
				//printf("IIII:%d\n",mp.finish);
				mp.success=0;
				//cp[index].status==3;//claw finish to rest
			}
		}
		/*else if(cp[index].status==3){
			if(round==cp[index].next_arr){
				if(queue[0]==0){
					printf("%d %d start playing\n",round,id);
					queue[0]++;
					queue[1]=id;
					cp[index].status=2;//rest to claw
				}
				//wait
				else{
					printf("%d %d wait in line\n",round,id);
					queue[queue[0]+1]=id;
					queue[0]++;
					cp[index].status=1;//rest to wait
				}
			}
		}*/
		sem_post(&(cp[index].sem));
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
	//file=argv[1];
	mp.occupy=0;
	mp.accumulate_fail=0;
	mp.success=0;
	mp.finish=0;
	//printf("enter file name:");
	//scanf("%s",file);
	FILE *fp,*out1,*out2;
	fp=fopen(argv[1],"r");

	sem_init(&all_finish,1,0);
	int var=0;
	int i=0;
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
		sem_init(&(cp[i].sem),1,0);
		sem_init(&(cp[i].machine_sem),1,1);
		cp[i].accumulate=0;
		cp[i].status=0;
		cp[i].conti_accum=0;
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
	pthread_create(&machine_thread,NULL,machine,(void*)cp);
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
