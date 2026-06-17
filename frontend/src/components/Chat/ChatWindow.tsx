import React from "react";
import { useAuth } from "../../hooks/useAuth";

export const ChatWindow: React.FC = () => {
  const { logout } = useAuth();

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h2>Chat</h2>
        <button onClick={logout}>Logout</button>
      </div>
      <div className="chat-messages">
        <p>Chat functionality coming soon...</p>
      </div>
    </div>
  );
};
