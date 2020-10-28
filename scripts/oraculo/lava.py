#!/usr/bin/python

import hashlib

"""
Python implementation of the lavarand n-way, sha-1, xor-rotate-and-fold
algorithm, aka. The Digital Blender (tm).
For details, see https://web.archive.org/web/20121015231322/http://www.lavarand.org/what/digital-blender.html
"""

###
BIG_FAT_DISCLAIMER = "Not 100% sure that this works, don't use it for anything real! (yet?)"
###

def n_way_turn(input, n=17):
    """Given a stream of octets, return n lists, with the input split across them.
    
    eg. input 00 01 02 03 04 05 06 07 08 with n=3 gives:
    00 03 06
    01 04 07
    02 05 08
    01, etc. are bytes, not strings or ints
    n=17 is given as a good default value by the lavarand docs.
    """
    # TODO: should we use zip()? Is there a DefaultList?

    # create n buffers
    buffer = [[] for x in range(n)]

    # push each byte into the relevant buffer
    for index, octet in enumerate(input):
        buffer[index % n].append(octet)

    # return the new bytes, as a binary string
    output = []
    for line in buffer:
        output.append(b''.join(i for i in line))
    return output


def sha1(inputs):
    """SHA-1 everything in the input list of strings."""
    return [hashlib.sha1(input).digest() for input in inputs]


def shift_left(byte):
    """Shift the byte left by one, and chop down to 8 bits."""
    return (byte << 1) & 255

def leftmost_bit(byte):
    """The leftmost (128-value) bit of the byte."""
    return byte & 128

def xor_fold_once(input, buffer):
    """xor input with the buffer and rotate the buffer one bit to the left."""
    ### /* xor the next SHA-1 digest chunk */
    output = [ord(a) ^ ord(b) for a, b in zip(input, buffer)]
    
    ### /* circular shift left by 1 bit */
    # whole buffer, not just individual bytes
    shifted = [chr(shift_left(output[i]) | leftmost_bit(output[i-1])) for i in range(len(output))]
    return shifted

def xor_fold_rot(buffers):
    """ Fold each buffer into the next with a xor-rotate-and-fold (not my terminology).""" 
    output = []

    # start with a buffer of null-bytes, then xor-fold it with 
    # the last buffer to initialize
    stored_buffer = chr(0) * 20
    stored_buffer = xor_fold_once(buffers[-1], stored_buffer)
    output.append(stored_buffer)

    # each buffer is then xor_folded with the previous one.
    for buffer in buffers:
        stored_buffer = xor_fold_once(buffer, stored_buffer)
        output.append(stored_buffer)

    return output


if __name__ == '__main__':
    for sources in [('SOLO', 'solo.png'), ('LAVA LAMP', 'lavalamp.png')]:
        print(sources[0])
        print('-' * len(sources[0]))
        print('')

	# run some "testing"
	# an octet is eight bits
	octets = file(sources[1], 'rb')

	# what do the octets look like?
	#print [ord(b) for b in octets.read(16)]
	#print n_way_turn(octets.read(24), n=3)
	assert n_way_turn('012345678', 3) == ['036', '147', '258'], n_way_turn('012345678', 3)
	
	blah = octets.read(24)
	#print blah
	#print "-" * 42
	#for line in n_way_turn(blah, n=3):
	    #print line, '\t', [ord(lb) for lb in line]
	    #print "-" * 42
	#print "-" * 42

	sha_thing = sha1( n_way_turn(blah, n=3) )
	#for t in sha_thing:
	    #print t
	    #print [ord(tb) for tb in t]
	#print [len(t) for t in sha_thing]

	#print "-" * 42

	#for byteline in xor_fold_rot(sha_thing):
	    #print byteline
	    #print [ord(b) for b in byteline]

	#print "-" * 42

	blah2 = octets.read(19200)
	#print "\n*** LOLBYTES" 
	#print n_way_turn(blah2, n=17)[0] 
	#print len(n_way_turn(blah2, n=17)[0])   # 1130 bytes
	big_blend = xor_fold_rot( sha1( n_way_turn(blah2, n=17) ) )
	#for byteline in big_blend:
	    #print byteline
	    #print ' '.join([str(ord(b)) for b in byteline])
	final_bytes = []
	for byteline in big_blend:
	    final_bytes.extend(byteline)
	print(''.join(hex(ord(b))[2:] for b in final_bytes))
	print('')

