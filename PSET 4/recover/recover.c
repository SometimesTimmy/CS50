#include <cs50.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>


int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("./recover [infile]\n");
        return 1;
    }

    // assign the 2nd argument as the infile to be opened
    char *infile = argv[1];
    FILE *file = fopen(infile, "r"); // infile for this HW is always card.raw

    // inform the user in the event that the forensic image cannot be opened
    if (file == NULL)
    {
        printf("Error opening the file card.raw\n");
        return 2;
    }

    // byte is an 8-bit unsigned number, from 0 to 255
    // digital cameras often initialize cards with a FAT file system whose "block size" is 512 bytes
    unsigned char buffer[512];

    // initialize the image files
    FILE* image = NULL;

    // initialize the counter for naming later
    int jpeg_count = 0; // increment by 1 as more jpegs are found

    // Start storing the jpegs that are found. A found = 0 would mean that at that state of the search, JPEG header condition is not yet foun.
    int found = 0; // will remain at 1 after a JPEG is found since we assume that the JPEGs are stored side by side.

    // Iterate through card.raw until there aren't anymore 512 byte blocks
    while (fread(buffer, 512, 1, file))
    {
        // all JPEGs have a distinct header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xe0) == 0xe0)
        {
            if (found == 1)
            {
                // JPEG header condition found. Close the image
                fclose(image);
            }
            else
            {
                found = 1;
            }

            // name the file with the format ###.jpg where ### starts at 000 and counts in the order of how it was found
            char filename[8];
            sprintf(filename, "%03d.jpg", jpeg_count);

            // open the next file in line with "write"
            image = fopen(filename, "w");
            jpeg_count++;
        }

        // once a JPEG header condition is found, start writing the file "image" (initialized earlier as NULL)
        if (found == 1)
        {
            fwrite(buffer, 512, 1, image);
            // no need to reset the variable "found" as 0 because we take advantage of the assumption that jpegs are stored "back to back"
        }
    }
    fclose(image);
    fclose(file);
    return 0;
}