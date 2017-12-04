#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        printf("./resize [int] [input file] [output file]\n");
        return 1;
    }

    // take in the 2nd command line argument as the factor of n
    int factor = atoi(argv[1]);

    // the first (n) must be a positive integer less than or equal to 100,
    if (factor > 100 || factor < 1)
    {
        printf("Factor must be a positive integer less than or equal to 100.\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // Everything up above this line except for the argv[1] has been "reading" codes from copy.c
    // Begin adjusting output file's file header and iteration codes.

    // all plain variabble's names are by default for the out file. In file will have _in

    // retain original dimensions
    int Width_in = bi.biWidth;
    int Height_in = bi.biHeight;

    // update width and height by the inputted factor
    bi.biWidth = Width_in*factor;
    bi.biHeight = Height_in*factor;

    // determine padding for scanlines
    int padding_in = (4 - (Width_in * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // update image size
    bi.biSizeImage = abs(bi.biHeight) * ((bi.biWidth * sizeof (RGBTRIPLE)) + padding);

    // update file size
    bf.bfSize = bi.biSizeImage + sizeof (BITMAPFILEHEADER) + sizeof (BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(Height_in); i < biHeight; i++)
		{
			// Write each line factor-times: vertical duplicates
			for(int y = 0; y < factor; y++)
			{
				// iterate over pixels in scanline
				for (int j = 0; j < Width_in; j++)
					{
					// temporary storage
					RGBTRIPLE triple;

					// read RGB triple from infile
					fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

					// write RGB triple to outfile: horizontal "stretch"
					for(int x = 0; x < factor; x++)
					    {
						fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
					    }
    			    }
				// skip over padding in infile
				fseek(inptr, padding_in, SEEK_CUR);

				// then add it to outfile
				for (int k = 0; k < padding; k++)
					{
						fputc(0x00, outptr);
                    }
				fseek(inptr, -(Width_in*3 + padding_in), SEEK_CUR);
			}
		fseek(inptr, Width_in*3 + padding_in, SEEK_CUR);
	}
	fclose(inptr);
	fclose(outptr);
	return 0;
}