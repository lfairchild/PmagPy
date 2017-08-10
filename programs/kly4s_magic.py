#!/usr/bin/env python
from __future__ import print_function
import sys
import pmagpy.command_line_extractor as extractor
import pmagpy.ipmag as ipmag

def main():
    """
    NAME
        kly4s_magic.py

    DESCRIPTION
        converts files generated by SIO kly4S labview program to MagIC formated
        files for use with PmagPy plotting software

    SYNTAX
        kly4s_magic.py -h [command line options]

    OPTIONS
        -h: prints the help message and quits
        -f FILE: specify .ams input file name
        -fad AZDIP: specify AZDIP file with orientations, will create er_samples.txt file
        -fsa SFILE: specify existing er_samples.txt file with orientation information
        -fsp SPFILE: specify existing er_specimens.txt file for appending 
        -F MFILE: specify magic_measurements output file
        -Fa AFILE: specify rmag_anisotropy output file
        -ocn ORCON:  specify orientation convention: default is #3 below -only with AZDIP file
        -usr USER: specify who made the measurements
        -loc LOC: specify location name for study 
        -ins INST: specify instrument used
        -spc SPEC: specify number of characters to specify specimen from sample
        -ncn NCON:  specify naming convention: default is #1 below

    DEFAULTS
        MFILE: magic_measurements.txt
        AFILE: rmag_anisotropy.txt
        SPFILE: create new er_specimens.txt file
        USER: ""
        LOC: "unknown" 
        INST: "SIO-KLY4S"
        SPEC: 1  specimen name is same as sample (if SPEC is 1, sample is all but last character)
    NOTES:
        Sample naming convention:
            [1] XXXXY: where XXXX is an arbitrary length site designation and Y
                is the single character sample designation.  e.g., TG001a is the
                first sample from site TG001.    [default]
            [2] XXXX-YY: YY sample from site XXXX (XXX, YY of arbitary length) 
            [3] XXXX.YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [4-Z] XXXXYYY:  YYY is sample designation with Z characters from site XXX
            [5] site name = sample name
            [6] site name entered in site_name column in the orient.txt format input file  -- NOT CURRENTLY SUPPORTED
            [7-Z] [XXX]YYY:  XXX is site designation with Z characters from samples  XXXYYY
            NB: all others you will have to either customize your
                self or e-mail ltauxe@ucsd.edu for help.

       Orientation convention:
            [1] Lab arrow azimuth= azimuth; Lab arrow dip=-dip
                i.e., dip is degrees from vertical down - the hade [default]
            [2] Lab arrow azimuth = azimuth-90; Lab arrow dip = -dip
                i.e., azimuth is strike and dip is hade
            [3] Lab arrow azimuth = azimuth; Lab arrow dip = dip-90
                e.g. dip is degrees from horizontal of drill direction
            [4] Lab arrow azimuth = azimuth; Lab arrow dip = dip 
            [5] Lab arrow azimuth = azimuth; Lab arrow dip = 90-dip 
            [6] all others you will have to either customize your
                self or e-mail ltauxe@ucsd.edu for help.

    """

    #def kly4s_magic(infile, specnum=0, locname="unknown", inst='SIO-KLY4S', samp_con="1", or_con='3' ,user='', measfile='magic_measurements.txt', aniso_outfile='rmag_anisotropy.txt', samp_infile='', spec_infile='', azdip_infile='', output_dir_path='.', input_dir_path='.'):
    args = sys.argv
    if '-h' in args:
        print(main.__doc__)
        sys.exit()
    dataframe = extractor.command_line_dataframe([['f', True, ''], ['fad', False, ''], ['fsa', False, ''], ['fsp', False, ''], ['Fsp', False, 'er_specimens.txt'], ['F', False, 'magic_measurements.txt'], ['Fa', False, 'rmag_anisotropy.txt'], ['ocn', False, '3'], ['usr', False, ''], ['loc', False, ''], ['ins', False, 'SIO-KLY4S'], ['spc', False, 0], ['ncn', False, '1'], ['WD', False, '.'], ['ID', False, '.'] ])
    checked_args = extractor.extract_and_check_args(args, dataframe)
    infile, azdip_infile, samp_infile, spec_infile, spec_outfile, measfile, aniso_outfile, or_con, user, locname, inst, specnum, samp_con, output_dir_path, input_dir_path = extractor.get_vars(['f', 'fad', 'fsa', 'fsp', 'Fsp', 'F', 'Fa', 'ocn', 'usr', 'loc', 'ins', 'spc', 'ncn', 'WD', 'ID'], checked_args)
    ipmag.kly4s_magic(infile, specnum=specnum, locname=locname, inst=inst, user=user, measfile=measfile,or_con=or_con, samp_con=samp_con, aniso_outfile=aniso_outfile, samp_infile=samp_infile, spec_infile=spec_infile, spec_outfile=spec_outfile, azdip_infile=azdip_infile, output_dir_path=output_dir_path, input_dir_path=input_dir_path)

    
if __name__ == "__main__":
    main()

