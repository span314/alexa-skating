# alexa-skating

Configuration to play skating music on the Echo Dot at the MIT rink. The setup is a combination of built-in music playing features and a custom Alexa skill. The built-in features are stable and more likely to work. The custom features are still in flux. Example usages are shown below with key words in **bold**. It works best if you speak loudly and enunciate.

### Playing ice dances (built-in)
* **Alexa, play Dutch Waltz playlist.**
* **Alexa, play** the **Rhythm Blues playlist.**
* **Alexa, shuffle Harris Tango playlist.**
* **Alexa, play Dutch Waltz** (not all dances)
* **Alexa, play Dutch Waltz 3** (not all dances)

Playlists contain official music from the [USFS solo dance](http://www.usfsa.org/programs?id=59305) site, which has all dances through gold and some of the international dances. The playlists match the dance name except a more specific name is required for the following dances: Keats Foxtrot, Dench Blues, Harris Tango, and Congelado. You may also request a dance without the playlist, but your mileage may vary depending on the dance name. Keep in mind that Alexa is matching against millions of songs in its database, so if you ask for Tango, it will likely pick the most popular tango or tango station.

### Playing song from prime music (built-in)
* **Alexa, play Shelter.**

### Playing from phone with Bluetooth (built-in)
* **Alexa, pair.**

### Playing Pandora radio (built-in)
* **Alexa**, play **Pandora**.
* **Alexa**, play **relaxation station on Pandora**.

### General playback control (built-in)
* **Alexa**, **stop**.
* **Alexa**, **pause**.
* **Alexa**, **continue**.
* **Alexa**, **repeat**.
* **Alexa**, **next** one.
* **Alexa**, **previous** one.

Alexa is pretty good about picking up various wordings of these commands, since the Echo was designed to be a music player.

### Playing program with delay (custom)
* **Alexa**, ask **skating helper** to **run** program **for Shawn**.
* **Alexa**, tell **skating helper run long for Flora**.
* **Alexa**, ask **skating helper** to **run** through **short** program **for Diane**.
* **Alexa**, open **skating helper** and **run** program **for Diane**.

Email me your music if you want to me to add it. Preferably, try using it two or three times and let Alexa fail finding your music so I can see how Alexa spells your name with your pronunciation in the logs.

### Playing program (custom)
* **Alexa**, ask **skating helper** to **play** program **for Shawn**.
* **Alexa**, tell **skating helper play long for Flora**.
* **Alexa**, ask **skating helper** to **play** through **short** program **for Diane**.
* **Alexa**, open **skating helper** and **play** music **for Diane**.

### Playing from an element (custom)
* **Alexa**, ask **skating helper** to **play** program **for Shawn from** the **step sequence**.

Tricky to get matching right for elements. Email me your Github username if you want to play around with this concept. Feel free to submit a PR with the logic you want. At least until this feature become more stable, I don't really want to customize things too much at this point.

### Contributing
If you want to mess around with the custom skill, email me your Github username and I'll add you. The first time you push anything, make sure you add your name to the license file. The high level picture is that the script uses the [Alexa Skills Kit](https://developer.amazon.com/alexa-skills-kit) and (partially) implements the [AudioPlayer Interface](https://developer.amazon.com/docs/custom-skills/audioplayer-interface-reference.html).