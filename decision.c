// Copyright © 2018 Brian Pomerantz. All Rights Reserved.

#include <stdio.h>

#define MAX_HAND_SIZE 21
#define NUM_HANDS 18
#define MAX(a, b) ((a > b) ? a:b)

struct hand {
    int arr[MAX_HAND_SIZE]
};

int newCard();
int runDealer(int pl, struct hand dl, int bet);
int handValue(struct hand h);
int handValueHelper(int *h);


int main(int argc, const char *argv[]) {
    int dlShow = atoi(argv[1]);
    int sims = atoi(argv[2]);
    double ev[NUM_HANDS];

    int i, j;
    struct hand dealer;

    for (i = 0; i < NUM_HANDS; i++) {
        int value = 0;
        for (j = 0; j < sims; j++) {
            dealer.arr[0] = dlShow;
            dealer.arr[1] = newCard();

            int k = 0;
            for (k = 2; k < MAX_HAND_SIZE; k++) {
                dealer.arr[k] = 0;
            }

            value += runDealer(i+4, dealer, 1);
        }

        ev[i] = ((double) value)/sims;

        printf("%d: %.3f\n", i+4, ev[i]);
    }
    
    return 0;
}

int newCard() {
    return rand() % 13 + 1;
}

int runDealer(int pl, struct hand dl, int bet) {
    dl.arr[1] = newCard();
    int i = 2;
    while (handValue(dl) < 17) {
        dl.arr[i] = newCard();
        i++;
    }

    int dlv = handValue(dl);

    if (dlv > 21) {
        return bet;
    }

    if (pl > dlv) {
        return bet;
    }
    else if (pl < dlv) {
        return -bet;
    }
    else {
        return 0;
    }
}

int handValue(struct hand h) {
    int hasAce = 0;
    int i = 0;
    for (i = 0; i < MAX_HAND_SIZE; i++) {
        if (h.arr[i] == 1) {
            hasAce = 1;
            break;
        }
    }

    int value = handValueHelper(h.arr);

    if (hasAce) {
        int v2 = value + 10;

        if (value > 21 && v2 < 21) {
            return v2;
        }
        else if (value < 21 && v2 > 21) {
            return value;
        }
        else {
            return MAX(value, v2);
        }
    }

    return value;
}

int handValueHelper(int *h) {
    int i;
    int value = 0;
    for (i = 0; i < MAX_HAND_SIZE; i++) {
        if (h[i] > 10) {
            value += 10;
        }
        else {
            value += h[i];
        }
    }

    return value;
}
