/* Message queue - header. */

#ifndef _MSG_QUEUE_H
#define _MSG_QUEUE_H

#include "fsk.h"
#include "Arduino.h"

// queue max size, bytes
#define QUEUE_SIZE 256
#define _QUEUE_SIZE_BITS (QUEUE_SIZE * 8L)

#define QUEUE_EMPTY -1

// how long it would take to send the whole queue
#define MS_TO_SEND_QUEUE (1000L * _QUEUE_SIZE_BITS / BITS_PER_SECOND)

/* how much we would like to refill the queue (higher
 * fractions mean we wait longer to refill)
 */
#define QUEUE_REFILL_FRACTION   0.95
#define QUEUE_REFILL_MS  (MS_TO_SEND_QUEUE * QUEUE_REFILL_FRACTION)

int queue_empty_spots();
bool enqueue(uint8_t item);
int dequeue();
int queue_count();

#endif
