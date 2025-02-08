'use client'

import { useState, useRef } from 'react';

let url = "http://localhost:8080/ask"

function Message(props){
	return <p>{props.message}</p>
}

function MessagesList(props){
	return (
		<div>
			{props.messages.map((message, index) => <Message key={index} message={message}/>)}
		</div>
	);
}

function MessageBox({ setMessages, messages }){
	const [buffer, setBuffer] = useState("");
	const inputRef = useRef();

	const click = async () => {
		let response = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ "question": buffer })
		});
		setBuffer("");
		inputRef.current.value = "";
		let data = await response.json();
		console.log(data, data.answer, data.content);
		setMessages([...messages, data.answer]);
	}; 

	return (
		<div>
			<input type="text" value={buffer} onChange={(e) => setBuffer(e.target.value)} ref={inputRef} placeholder="Type your question..."/>
			<button onClick={click}>Send</button>
		</div>
	);
}

export default function Home() {
	const [messages, setMessages] = useState(["oi"]);	

  	return (
		<main>
			<MessagesList messages={messages}/>
			<MessageBox setMessages={setMessages} messages={messages}/>
		</main>
  );
};
