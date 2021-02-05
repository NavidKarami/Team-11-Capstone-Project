/* 
 * Tamarr Stigler 
 * Menu [Code] 
 * Objecitve: Asking user for the name 
 * Version 1 (1/5/2021)
 */ 


// Libaries 
#include <stdio.h> 
#include <string.h>
// Define 

// Predefine Functions
void NEW();
void CURRENT();

int main() {

	char user[100];
	char new[10] = "new";
	char current[10] = "current";
	printf("***** MENU *****\n");
	
	printf("\n");
	printf("Are you a current user?\n");
	printf("Are you a new user?\n");
	printf("\n");

	printf("Please type [current] if you are a current user.\n");
	printf("Please type [new] if you are a new user.\n");
	printf("\n");

	scanf("%s", user);
	printf("Based on what you entered, you entered %s.\n", user);
	printf("\n");

	if(strcmp(user,new) == 0){
		printf("Excellent, welcome! Lets create you as a new user!\n");
		NEW();
	}

	else if(strcmp(user,current) == 0){
		printf("Excellent, welcome!\n");
		//CURRENT();
	}
	else 
		printf("Invalid input, please try again.\n");

	//Go to Current Module 
	
	//Go to New Module 

	return 0;
}


void NEW() {

	char name[100];
	int pincode, pincode2;

	printf("Since you are a new user, please type in your name\n");
	scanf("%s", name);

	printf("Welcome, %s\n", name);

	/*Ask the user to speak a phase*/

	/*Ask the user for a four-digit pin code*/ 
	printf("Please create a four-digit pin code.\n");
	scanf("%d", &pincode);
	//printf("%d\n", pincode);
	printf("\n");
	
	printf("Please confirm your four-digit pin code.\n");
	scanf("%d", &pincode2);
	
	if(pincode == pincode2)
		printf("Congrats you entered a vaild four-digit pin code.\n");
	else
		printf("Pincode does not match try again.\n");

	
}

