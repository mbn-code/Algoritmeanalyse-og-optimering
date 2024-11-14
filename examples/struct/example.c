/**
 * @brief A structure to hold identity information.
 * 
 * This structure contains an integer ID and a character Grade.
 * It can be used to store and manage identity-related data.
 */

/*
Now this is important to showcase becuase in algorithm optimization in embedded software
we look at not just how much memory we are using but also when we are allocating which bytes and where
*/

struct {
    int ID; // uses 4 bytes 
    char Grade; // uses 1 byte
} Identity;

/*
We do it like this because we want to optimize memory usage based on the 
memory padding and alignment.
The compiler will add padding to make sure that the data is aligned.
This is important because the CPU can access the data faster if it is aligned.
But not faster if if is aligned but too much padding is added.
*/

/*
Second example.
Placing the char first often requires 3 additional bytes of padding before the int to align ID to a 4-byte boundary. This increases the size of the struct and wastes memory.
*/
struct {
    char Grade; // 1 byte
    int ID;     // 4 bytes
} Identity;
