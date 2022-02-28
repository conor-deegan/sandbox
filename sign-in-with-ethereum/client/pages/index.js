import { useEffect, useState } from 'react';
import axios from 'axios';
import Web3 from 'web3';

export default function Home() {
  const [account, setAccount] = useState('');
  const [web3, setWeb3] = useState('');

  const api = {
    getMessage: async (account) => {
      return axios.get(`http://localhost:8080/message/${account}`);
    },
  };

  const connect = async () => {
    try {
      if (
        typeof window === 'undefined' ||
        typeof window.ethereum === 'undefined'
      ) {
        console.log('Please download MetaMask');
        return;
      }
      await window.ethereum.request({
        method: 'eth_requestAccounts',
      });
      const web3 = new Web3(window.ethereum);
      const accounts = await web3.eth.getAccounts();
      setWeb3(web3);
      setAccount(accounts[0]);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    connect();
  }, []);

  const handleLoginClick = async () => {
    const { data: message } = await api.getMessage(account);
    console.log(message);
  };

  return (
    <main>
      <h1>Sign-in with Ethereum</h1>
      <button onClick={handleLoginClick}>Login</button>
    </main>
  );
}
