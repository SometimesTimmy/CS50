#include <stdio.h>
#include <cs50.h>
#include <math.h>

long long Number; //credit card number
long long n_count;
int digits;

long long Number1; //every other digit starting with the last digit
int n1;
int sum_n1;

long long Number2; //every other digit starting with the second to last digit
int n2;
int sum_n2;

int main (void)
{
       printf("Number: ");
       Number = get_long_long();
       if (Number < 0)
       {
           printf("INVALID\n");
       }

       // n_count is a dummy copy for counting digit length //
       n_count = Number;
       // digits is the counter //
       digits = 0;
       while (n_count >= 1)
       {
           n_count = n_count / 10;
           digits = digits + 1;
       }
       //printf("card length is %i\n", digits); used during testing

       if ((digits != 13) && (digits != 15) && (digits != 16))
       {
           printf("INVALID\n");
       }

       //n2 is the individual ever other digit starting with the second to last digit
       n2 = 0;
       sum_n2 = 0;
       //Number2 is the dummy copy for n2
       Number2 = (Number - Number%10)/10;
       while (Number2 > 1)
       {
           n2 = Number2%10;
           Number2 = Number2/100;
           if (n2*2==10)
           {
               sum_n2 = sum_n2 + 1;
           }
           if (n2*2<10)
           {
               sum_n2 = sum_n2 + n2*2;
           }
           if (n2*2>10)
           {
               sum_n2 = sum_n2 + n2*2%10 + 1;
           }
       }
       // printf("sum of all n2 is %i\n",sum_n2);

       //n1 is the individual ever other digit starting with the last digit
       n1 = 0;
       //Number1 is the dummy copy for n1
       Number1 = Number;
       while (Number1 > 0)
       {
           n1 = Number1%10;
           Number1 = Number1/100;
           sum_n1 = sum_n1 + n1;

       }
       // printf("sum of all n1 is %i\n",sum_n1);
       // printf("sum of sum_n1 and sum_n2 is %i\n",sum_n1+sum_n2);
       if ((sum_n1+sum_n2)%10 != 0)
       {
           printf("INVALID\n");
       }

       //American Express uses 15-digit numbers, MasterCard uses 16-digit numbers, and Visa uses 13- and 16-digit numbers
       if (digits == 15)
       {
              if((Number >= 340000000000000 && Number < 350000000000000) || (Number >= 370000000000000 && Number < 380000000000000))
              {
                     printf("AMEX\n");
              }
              else
              {
                     printf("INVALID\n");
              }
       }
       if (digits == 16)
       {
           //MasterCard numbers all start with 51, 52, 53, 54, or 55
           //Visa numbers all start with 4
           if(Number >= 5100000000000000 && Number < 5600000000000000)
           {
                  printf("MASTERCARD\n");
           }
           else if(Number/1000000000000000 < 5)
           {
                  printf("VISA\n");
           }
           else
           {
                  printf("INVALID\n");
           }
       }
       if(digits == 13)
       {
              if(Number/1000000000000 < 5)
              {
                     printf("VISA\n");
              }
              else
              {
                     printf("INVALID\n");
              }
       }
}