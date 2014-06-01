jQuery(function ($)
       {
           // You can determine if we are currently in the game by checking the jsapi object
           var runningInGame = typeof window.jsapi != "undefined";

           $("button").button();

           $("button-quit-game").button().click(function(event)
                                                {
                                                    event.preventDefault();

                                                    window.menuAPI.quit();
                                                });
       });
