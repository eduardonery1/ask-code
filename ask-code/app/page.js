'use client'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useState, useRef } from 'react';

let url = process.env.SERVER_HOST || "http://localhost:8080/ask"

function SystemMessage({ content }){
	let codeDelimiter = "```";
	const parts = content.split(codeDelimiter);
	let formattedContent = [];

	for (let i = 0; i < parts.length; i++) {
		if (i % 2 === 0) {
			// Regular text
			formattedContent.push(<span key={i}>{parts[i]}</span>);
		} else {
			// Code block
			const code = parts[i];
			let idx = code.search("\n"); //First space is after the language
			let language = code.substr(0, idx);
			console.log(language)
			formattedContent.push(
				<SyntaxHighlighter language={language} style={vscDarkPlus} key={i} className="rounded-lg">
					{code.substr(idx+1)}
				</SyntaxHighlighter>
			);
		}
	}
	return (
		<div className="flex justify-start items-start gap-2">
			<div className="bg-blue-900 p-1 rounded-lg min-w-[30%] max-w-[80%] break-words overflow-y-auto text-white">
				{formattedContent}
			</div>
		</div>
	);
}

function UserMessage({ content }){
	return (
		<div className="flex justify-end items-end bg-grey-500 gap-2 m-2">
			<div className="bg-blue-600 p-2 min-w-[30%] max-w-[60%] break-words overflow-y-auto text-white rounded-lg ">
				{content}
			</div>
		</div>
	);
}

function MessagesList({ messages }){
	return (
	<div className="p-8 overflow-auto bg-gray-900 w-full h-[80vh] sm:h-[90vh] flex-col justify-center overflow-auto gap-2">
			{	
				messages.map(
					(message, index) => (message.sender === "system")? <SystemMessage key={index} content={message.content}/> 
														      : <UserMessage key={index} content={message.content}/>
				)
			}
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
