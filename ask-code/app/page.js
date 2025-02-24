'use client'

import { useState, useRef } from 'react';

let url = process.env.SERVER_HOST || "http://localhost:8080/ask"

function Message({ message }){
	let isSystem = message.sender ==="system";
	let outter_class = (isSystem)? " justify-start items-start left-0 " : " justify-end items-end";
	let inner_class = (isSystem)? " bg-blue-500 " : " bg-blue-700 ";
	let regex = "```";
	let parts = message.content.split(regex);

	return (
		<div className={"flex " + outter_class + "bg-grey-500 gap-2"}>
			<div className={inner_class + "p-2 min-w-[30%] max-w-[50%] break-words overflow-y-auto text-white rounded-lg "}>
				{parts.map((part, index) => {
					if (index % 2 === 0) {
						return (<span key={index}>{part}</span>);
					} else {
						return (<code key={index}>{part}</code>);
					}
				})}
			</div>
		</div>
	);
}


function MessagesList(props){
	return (
	<div className="p-8 overflow-auto bg-gray-900 w-full h-[80vh] sm:h-[90vh] flex-col justify-center overflow-auto gap-2">
			{props.messages.map((message, index) => <Message key={index} message={message}/>)}
	</div>
	);
}

function MessageBox({ setMessages, messages }){
	const [buffer, setBuffer] = useState("");

	const click = async (value) => {
		let newMessageList = [...messages, {"sender": "user", "content": value}];
		setMessages(newMessageList)

		let response = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ "question": value })
		});

		let data = await response.json();
		//console.log(data, data.answer, data.content);
		newMessageList.push({"sender": "system", "content": data.answer});
		setMessages([...newMessageList]);
	}; 

	return (
		<div className="fixed bottom-0 w-full bg-gray-300 h-[20vh] sm:h-[10vh] border-gray-300 p-1 flex justify-center items-center gap-2 ">
			<textarea 
				className="border rounded-sm overflow-hidden w-[80vw] h-[100%] bg-gray-200" 
				type="text" 
				value={buffer} 
				onChange={(e) => setBuffer(e.target.value)} 
				placeholder="Type your question..."
				onKeyDown={(e) => {
					if (e.key === "Enter" && !e.shiftKey) { 
						e.preventDefault();
						if (buffer.trim()){
							click(buffer);
							setBuffer("");
						}
					}} }
			/>
		</div>
	);
}

export default function Home() {
	const [messages, setMessages] = useState([{"sender": "system", "content": "Ask me a programming question!"}]);	
  	return (
		<main>
			<MessagesList messages={messages}/>
			<MessageBox setMessages={setMessages} messages={messages}/>
		</main>
  );
};
