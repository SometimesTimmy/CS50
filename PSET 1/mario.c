#include <stdio.h>
#include <cs50.h>

int Height;
int i;
int j;
int k;
int l;

int main (void) 
{
   do 
   {
       printf("Height: ");
       Height = get_int();
       if (Height == 0)
       {
          return 0;
       }
   }
   while ( Height < 1 || Height > 23 );
   for (i = 0; i < Height; i++)
   {
      for (j = 0; j < Height-i-1;  j++)
      {
         printf(" ");
      }
      for (k = 0; k < i+1; k++)
		{
			printf("#");
		}
		   printf("  ");
		for (l = 0; l < i+1; l++)
		{
			printf("#");
		}
   printf("\n");
   }
}