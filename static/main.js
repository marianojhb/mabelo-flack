document.addEventListener("DOMContentLoaded", function() {
  // Task: To color active links and add sronly
  // ------------------------------------------

  // Check if actual page is contained in nav menu links
  let navlinks = document.querySelectorAll(".nav-item a");
  let navlinkslengh = navlinks.length;
  let alinks = []; // THE array of links
  navlinks.forEach(item => {
    alinks.push("/" + item.href.split("/")[navlinkslengh - 1]);
  }); // now we have an array "alinks" with each link of nav menu items

  // If actual page is contained in nav menu links ("alinks"), then color that link!
  let path = window.location.pathname; // saves current page URL
  if (alinks.includes(path)) {
    document
      .querySelector('.nav-item a[href="' + path + '"]')
      .parentNode.classList.add("active");
    let sronly = '<span class="sr-only">(current)</span>';
    document
      .querySelector('.nav-item a[href="' + path + '"]')
      .insertAdjacentHTML("beforeend", sronly);
  }


  // Add new channel
  if (path == "/channels") {
    document.querySelector("#addchannel").onsubmit = () => {
      // AJAX
      const request = new XMLHttpRequest();
      const channelname = document.querySelector("#channelname").value;
      request.open("POST", "/retrievechannels");
      document.querySelector(
        "#channel_added_message"
      ).innerHTML = `<p>Channel "<b>${channelname}</b>" added.<p>`;
      document.querySelector("#channelname").value = "";

      request.onload = () => {
        const datos = JSON.parse(request.responseText);
        let channellist = "";
        if (datos.success) {
          for (let el of datos.data["channels"]) {
              channellist += `<a href="/channels/${el.channel}" class="badge col-sm-3 col-lg-2 mb-2 mx-1 p-2 ${el.color}">${el.channel}</a>`;
          }
        }

        document.querySelector("#channels").innerHTML = channellist;
      };
      const data = new FormData();
      data.append("channelname", channelname);
      request.send(data);
      return false;
    };
  }

  // Welcome and sign in
  if (path == "/") {
    if (document.querySelector("#welcome") == null) {
      document.querySelector("#signin").onsubmit = () => {
        const request = new XMLHttpRequest();
        const displayname = document.querySelector("#displayname").value;
        if (displayname.trim().length == 0) {
          displayname = "";
          return false;
        }
        request.open("POST", "/login");

        // When receiving JSON response, redirect to channels section
        request.onload = () => {
          const data = JSON.parse(request.responseText);
          setInterval(gotochannels, 1500);
          function gotochannels() {
            location.href = "/channels";
          }
        };
        const data = new FormData();
        data.append("displayname", displayname);
        localStorage.setItem("displayname", displayname);
        request.send(data);
        return false;
      };
    }
  }

  // If we are in some channel, execute the following code:
  if (path == "/channels/" + document.location.pathname.split("/")[2]) {
    // Connect to websocket
    var socket = io.connect(
      location.protocol + "//" + document.domain + ":" + location.port
    );

    // When connected, send message to server
    socket.on("connect", () => {
      // Each button should emit a "submit vote" event
      document.querySelector("#btn_send").onclick = () => {
        const message = document.querySelector("#message").value;
        document.querySelector("#message").value = "";
        socket.emit("submit message", {'message': message });
      };
    });

    // When a message is broadcasted, add to the chat window
    socket.on("announce message", data => {
      const p = document.createElement("p");
      p.innerHTML = `${data.displayname} (${data.timestamp}): ${data.message} `;
      document.querySelector("#chat").append(p);
      
      //Scroll to bottom after sending message
      document.querySelector("#chat").scrollTop = 10000;
    });

    // Scroll to bottom when loading chat:
    document.querySelector("#chat").scrollTop = 10000;

  }
});
