//+------------------------------------------------------------------+
//|                                              AccountBalanceEA.mq4|
//|                        Copyright 2023, MetaQuotes Software Corp.  |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "2023, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict

int OnInit()
  {
   EventSetTimer(10); // Set the timer to call OnTimer() every 10 seconds
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   EventKillTimer(); // Kill the timer when the EA is removed
  }

void OnTimer()
  {
   double balance = AccountBalance();
   string file_name = "AccountBalance.txt";
   int file_handle = FileOpen(file_name, FILE_WRITE|FILE_TXT);
   
   if(file_handle != INVALID_HANDLE)
     {
      FileWrite(file_handle, balance);
      FileClose(file_handle);
     }
   else
     {
      Print("Failed to open file for writing");
     }
  }

void OnTick()
  {
   // Not used in this example
  }
//+------------------------------------------------------------------+
