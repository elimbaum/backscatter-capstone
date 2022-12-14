/* Message queue. */

#include "msg_queue.h"

// location of the START of the queue
int queue_head = 0;
// location of the LAST ELEMENT of the queue
int queue_tail = 0;
int _queue_count = 0;

uint8_t queue[QUEUE_SIZE];

bool queue_is_full() {
  return _queue_count == QUEUE_SIZE;
}

bool queue_is_empty() {
  return _queue_count == 0;
}

int queue_empty_spots() {
  return QUEUE_SIZE - _queue_count;
}

int queue_count() {
  return _queue_count;
}

// TODO: prevent race condition, maybe need a lock
bool enqueue(uint8_t item) {
  if (queue_is_full()) {
    // no more room.
    Serial.print("Qf");
    return false;
  }

  if (queue_tail >= QUEUE_SIZE - 1) {
    queue_tail = -1;
  }
  queue[++queue_tail] = item;

  noInterrupts();
  _queue_count++;
  interrupts();

  return true;
}

void enqueue_block(uint8_t item) {
  while (queue_is_full()) { }

  enqueue(item);
} 

int dequeue() {
  if (queue_is_empty()) {
    return QUEUE_EMPTY;
  }

  uint8_t item = queue[queue_head++];
  if (queue_head >= QUEUE_SIZE) {
    queue_head = 0;
  }

  noInterrupts();
  _queue_count--;
  interrupts();

  return item;
}
