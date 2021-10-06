/* Message queue - header. */

#include "fsk.h"

// queue max size, bytes
#define QUEUE_SIZE 256

#define _QUEUE_SIZE_BITS (QUEUE_SIZE * 8L)

#define MS_TO_SEND_QUEUE (1000L * _QUEUE_SIZE_BITS / BITS_PER_SECOND)
#define QUEUE_REFILL_MS  (MS_TO_SEND_QUEUE / 2)
