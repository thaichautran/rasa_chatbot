import "./chatBot.css";
import { useEffect, useState } from "react";

function Basic() {
  const [chat, setChat] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [botTyping, setbotTyping] = useState(false);

  useEffect(() => {
    const objDiv = document.getElementById("messageArea");
    objDiv.scrollTop = objDiv.scrollHeight;
  }, [chat]);

  const handleSubmit = (evt) => {
    evt.preventDefault();
    const name = "thaichau";
    const request_temp = { sender: "user", sender_id: name, msg: inputMessage };

    if (inputMessage !== "") {
      setChat((chat) => [...chat, request_temp]);
      setbotTyping(true);
      setInputMessage("");
      rasaAPI(name, inputMessage);
    } else {
      window.alert("Vui lòng nhập input");
    }
  };

  const rasaAPI = async (name, msg) => {
    //chatData.push({sender : "user", sender_id : name, msg : msg});

    await fetch("http://localhost:5005/webhooks/rest/webhook", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        charset: "UTF-8",
      },
      credentials: "same-origin",
      body: JSON.stringify({ sender: name, message: msg }),
    })
      .then((response) => response.json())
      .then((response) => {
        console.log(response);
        if (response) {
          // const temp = response[0];
          // const recipient_id = temp["recipient_id"];
          // const recipient_msg = temp["text"];

          // const response_temp = {
          //   sender: "bot",
          //   recipient_id: recipient_id,
          //   msg: recipient_msg,
          // };
          // setbotTyping(false);

          // setChat((chat) => [...chat, response_temp]);
          response.forEach((res, index) => {
            const temp = response[index];
            const recipient_id = temp["recipient_id"];
            const recipient_msg = temp["text"] ? temp["text"] : temp["image"];

            const response_temp = {
              sender: "bot",
              recipient_id: recipient_id,
              msg: recipient_msg,
            };
            setbotTyping(false);

            setChat((chat) => [...chat, response_temp]);
          });
          // scrollBottom();
        }
      });
  };

  const stylecard = {
    maxWidth: "35rem",
    paddingLeft: "0px",
    paddingRight: "0px",
    margin: "0 auto",
    borderRadius: "30px",
    boxShadow: "0 16px 20px 0 rgba(0,0,0,0.4)",
    background: "#7F7FD5",
  };
  const styleHeader = {
    padding: "1rem",
    borderRadius: "30px 30px 0px 0px",
    backgroundColor: "rgba(0,0,0,0.3)",
  };
  const styleFooter = {
    padding: "0.75rem 0 0.75rem 1rem",
    borderRadius: "0px 0px 30px 30px",
    backgroundColor: "rgba(0,0,0,0.3)",
  };
  const styleBody = {
    padding: "1.2rem",
    height: "65vh",
    overflowY: "a",
    overflowX: "hidden",
    backgroundColor: "rgba(0,0,0,0.4)",
  };

  console.log(chat);
  return (
    <div>
      {/* <button onClick={() => rasaAPI("shreyas", "hi")}>Try this</button> */}

      <div className="container">
        <div className="row justify-content-center">
          <div className="card" style={stylecard}>
            <div className="cardHeader text-white" style={styleHeader}>
              <h1 style={{ marginBottom: "0px" }}>Chatbot Assistant</h1>
            </div>
            <div className="cardBody" id="messageArea" style={styleBody}>
              <div className="row msgarea">
                {chat.map((user, key) => (
                  <div key={key}>
                    {user.sender === "bot" ? (
                      <div className="msgalignstart">
                        <div>
                          <img
                            src="https://i.pinimg.com/originals/bf/c2/d5/bfc2d545085d92374c5d1504e6cab298.gif"
                            alt="botimg"
                            className="img-fluid botIcon"
                          />
                        </div>
                        <h5
                          className="botmsg"
                          style={{
                            marginBottom: 0,
                            marginLeft: "0.5rem",
                            fontSize: 16,
                          }}
                        >
                          {user.msg.includes("https://") ? (
                            <img
                              src={user.msg}
                              alt="img-res"
                              className="img-fluid"
                            />
                          ) : (
                            user.msg
                          )}
                        </h5>
                      </div>
                    ) : (
                      <div className="msgalignend">
                        <h5
                          className="usermsg"
                          style={{
                            marginBottom: 0,
                            marginRight: "0.5rem",
                            fontSize: 16,
                          }}
                        >
                          {user.msg}
                        </h5>
                        <div>
                          <img
                            src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg"
                            alt="userimg"
                            className="img-fluid userIcon"
                          />
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
              {botTyping ? (
                <div className="msgalignstart">
                  <div>
                    <img
                      src="https://i.pinimg.com/originals/bf/c2/d5/bfc2d545085d92374c5d1504e6cab298.gif"
                      alt="botimg"
                      className="img-fluid botIcon"
                    />
                  </div>
                  <h5
                    className="botmsg"
                    style={{
                      marginBottom: 0,
                      marginLeft: "0.5rem",
                      fontSize: 16,
                    }}
                  >
                    typing...
                  </h5>
                </div>
              ) : null}
            </div>
            <div className="cardFooter text-white" style={styleFooter}>
              <div className="row">
                <form
                  style={{ display: "flex", alignItems: "center" }}
                  onSubmit={handleSubmit}
                >
                  <div className="col-10" style={{ paddingRight: "0px" }}>
                    <input
                      onChange={(e) => setInputMessage(e.target.value)}
                      value={inputMessage}
                      type="text"
                      className="msginp"
                    ></input>
                  </div>

                  <div className="col-2">
                    <button type="submit" className="circleBtn">
                      <div>
                        <img
                          src="https://cdn-icons-png.flaticon.com/512/2099/2099085.png"
                          alt="sendImg"
                          className="sendBtn"
                        />
                      </div>
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Basic;
