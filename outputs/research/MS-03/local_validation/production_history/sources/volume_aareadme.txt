PDS_VERSION_ID         = PDS3
RECORD_TYPE            = STREAM
OBJECT                 = TEXT
  PUBLICATION_DATE     = 2022-06-20
  INTERCHANGE_FORMAT   = ASCII
  NOTE                 = "N/A"
END_OBJECT             = TEXT
END


Mars Reconnaissance Orbiter (MRO) Compact Reconnaissance Imaging Spectrometer
for Mars (CRISM) Data Archive


1.  Introduction

This archive contains data acquired by the Mars Reconnaissance Orbiter (MRO)
Compact Reconnaissance Imaging Spectrometer for Mars (CRISM) instrument.

2.  File Formats

This section describes the format of CRISM Archive Volumes. Data that
comprise the Archive will be formatted in accordance with Planetary Data
System standards.

2.1. Disk Format
  Archive Volumes are formatted so that when written to CD or DVD media
according to PDS policy, the media are compatible with most commonly used
computer operating systems including Windows, Unix, and Macintosh systems.
The CD volume format is in accordance with ISO 9660 level 2 Interchange
Standard. The DVD volume format is in accordance with the UDF Standard with
ISO 9660 Level 2 compatibility.
 
2.2. File Formats
  This section describes file formats for the kinds of files contained on
Archive Volumes.
 
2.2.1. Document File Formats
  Document files with the .TXT suffix exist in the ROOT, INDEX, CATALOG,
DOCUMENT, and BROWSE directories. They are ASCII files which may have 
embedded PDS labels. Lines in a .TXT file end with a carriage return 
character (ASCII 13) and a line feed character (ASCII 10). This allows the 
files to be readable under various operating systems.
  Some documents in the DOCUMENT directory contain formatting and figures 
that cannot easily be rendered as ASCII text. Therefore each document is 
given in PDF format. PDF (Portable Document Format) is a proprietary format 
of Adobe Systems Incorporated that is frequently used for distributing
documents. Adobe offers free software, Acrobat Reader, for viewing PDF files.
Some type of ASCII text versions of these documents will also be included,
possibly using HTML or XML, in order to meet the PDS requirement that
documents must be archived as ASCII text.

2.2.2. Tabular File Format
  Tabular files (.TAB suffix) exist in the INDEX and MRDR directories. 
Tabular files are ASCII files formatted for direct reading into many 
database management systems on various computers. All fields are separated 
by commas. (Character fields are padded with spaces to keep quotation marks 
in the same columns of successive records.) Character fields are left 
justified, and numeric fields are right justified. The "start byte" listed 
in the labels indicate the starting position in bytes of each field in a 
record; the field length "bytes" does not include the commas between fields. 
The records are of fixed length, and the last two bytes of each record 
contain the ASCII carriage return and line feed characters. This allows a 
table to be treated as a fixed length record file on computers that support 
this file type and as a text file with embedded line delimiters on those 
that don't.
  Every CRISM tabular file is described by a detached PDS label with the same
name as the data file it describes, and the extension .LBL. For example, the
file INDEX.TAB is accompanied by the detached label file INDEX.LBL in the
same directory.

2.2.3. PDS Label Format
  All data files in CRISM the archive have PDS labels detached in a separate
file. For examples of PDS labels for each type of data product, see the Data
Product SIS in the DOCUMENT directory.
  A PDS label provides descriptive information about the associated file. The
PDS label is an object-oriented structure consisting of sets of
'keyword=value' declarations. The object to which the label refers (e.g.
IMAGE, TABLE, etc.) is denoted by a statement of the form:
    ^object = location
in which the carat character (^, also called a pointer in this context)
indicates where to find the object. In an embedded label, the location is an
integer representing the starting record number of the object (the first
record in the file is record 1). In a detached label, the location denotes
the name of the file containing the object, along with the starting record or
byte number, if there is more than one object in the file. For example:
    ^HEADER = ("F01.IMG",1)
    ^IMAGE = ("F01.IMG",1025 <BYTES>)
indicates that the IMAGE object begins at byte 1025 of the file F01.IMG, in
the same directory as the detached label file. Below is a list of the 
possible formats for the ^object definition.
    ^object = n
    ^object = n<BYTES>
    ^object = "filename.ext"
    ^object = ("filename.ext",n)
    ^object = ("filename.ext",n<BYTES>)
where
    n is the starting record or byte number of the object, counting from the
      beginning of the file (record 1, byte 1),
    <BYTES> indicates that the number given is in units of bytes,
    filename is the up to 28 character, alphanumeric upper-case file name,
    ext is the 3 character upper-case file extension
  Lines of text in detached labels end with a carriage return character
(ASCII 13) and a line feed character (ASCII 10). This allows the files to be
readable under various operating systems.

2.2.4. Catalog File Format
  Catalog files (suffix .CAT) exist in the ROOT and CATALOG directories. They
are text files formatted in an object-oriented structure consisting of sets
of 'keyword=value' declarations, so that they are readable by humans and by
software.
 
2.2.5. Science Data File Formats
  For more information about the format and content of the data products, see
the discussions in the CRISM Data Product and Archive Volume SISs located in
the DOCUMENT directory. 

3.  Archive Contents

Files in this archive are organized into a series of subdirectories below the
top-level directory.  The archive organization and the contents of each
directory are described below.

Top-level Directory
-------------------

AAREADME.TXT

The file you are currently reading.

ERRATA.TXT

This text file contains a listing of comments and updates concerning the
archive volume.

VOLDESC.CAT

This text file contains a description of the volume contents as a PDS catalog
object.  It is a required file on PDS archive volumes.

MRDR Directory
--------------

The MRDR directory contains CRISM Multispectral Reduced Data Records (MRDRs).
See MRDR_DS.CAT for details.

INDEX Directory
---------------

The INDEX directory contains PDS index files for this archive.  An index
file is an ASCII table with each record (or line) in the table containing
information about a single data product in archive.  Files in the Index
directory are provided to help the user locate products on the archive
volume. See the file INDXINFO.TXT for additional details.

DOCUMENT Directory
------------------

The DOCUMENT directory contains contains documentation to help the user
understand and use the archive data. See DOCINFO.TXT for a description of the
files in the DOCUMENT directory.

CATALOG Directory
-----------------

The files in the CATALOG Directory provide a top-level understanding of the
mission, spacecraft, instruments, and data set. The files in this directory
become part of the PDS Catalog to provide background information for the user
searching for data. Their format and contents are further specified in the
PDS Standards Reference. See the file CATINFO.TXT for details.

BROWSE Directory
------------------

The BROWSE directory contains synoptic versions of data products to help
identify products of interest.  See BROWINFO.TXT for more information.

4.  Whom to Contact for Information

For questions concerning this volume set, contact:

    PDS Geosciences Node
    Washington University
    1 Brookings Drive, Campus Box 1169
    St. Louis, MO  63130
    314-935-9295

    Web Site:  http://pds-geosciences.wustl.edu/
    E-mail:    geosci@wunder.wustl.edu

For general information related to the PDS, contact:

    Planetary Data System, PDS Operator
    M/S 202-101
    Jet Propulsion Laboratory
    4800 Oak Grove Drive
    Pasadena, CA  91109-8099
    (818) 354-4321

    WWW Site:  http://pds.jpl.nasa.gov/
    E-mail:    pds_operator@jpl.nasa.gov

5.  Cognizant Persons

This archive volume designed and produced at the PDS Geosciences Node,
Washington University, St. Louis, Missouri by Jennifer Ward and Susan
Slavney.
