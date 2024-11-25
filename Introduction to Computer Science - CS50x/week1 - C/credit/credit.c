#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long n = get_long("Card's number: ");

           if ( (339999999999999 < n && n < 350000000000000) || (369999999999999 < n && n < 380000000000000) )
                {
                    printf ("AMEX\n");
                }
                else if ( 5099999999999999 < n && n < 5600000000000000 )
                    {
                        printf ("MASTERCARD\n");
                    }
                    else if ( (3999999999999 < n && n < 5000000000000) || (3999999999999999 < n && n < 5000000000000000))
                        {
                            printf ("VISA\n");
                        }
                            else
                            {
                                printf ("INVALID\n");
                            }
}