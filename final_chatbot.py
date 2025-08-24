from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path

class SimpleChatbot:
    def get_response(self, query):
        query = query.lower().strip()
        
        if any(word in query for word in ['hello', 'hi', 'hey']):
            return "Hey there! 👋 I'm your friendly company assistant. What can I help you with today?"
        
        elif any(word in query for word in ['company', 'about', 'what is']):
            return "We're a tech company building innovative solutions! 🚀 We focus on making technology accessible and useful for everyone. Want to know about our work culture, benefits, or processes?"
        
        elif any(word in query for word in ['work', 'hours', 'remote']):
            return "Here's our work setup! ⏰ Standard hours are 9 AM-5 PM EST, but we're flexible! Remote work is supported 3 days/week. We believe in work-life balance! 🏡"
        
        elif any(word in query for word in ['benefits', 'insurance', 'vacation']):
            return "Our benefits are awesome! 🎉 100% health insurance covered, 401k matching up to 6%, 25 days vacation + 10 sick days, $3K professional development budget, and gym reimbursement!"
        
        elif any(word in query for word in ['refund', 'expense', 'reimburse']):
            return "Expense reimbursement is easy! 💰 Submit receipts within 30 days, get reimbursed for travel, home office setup ($1.5K), and business expenses. Just keep those receipts!"
        
        elif any(word in query for word in ['design', 'logo', 'brand']):
            return "Need design assets? 🎨 Find logos in /Marketing/Brand, brand guidelines on our wiki, or submit requests to design@company.com. Turnaround is 3-5 days!"
        
        elif any(word in query for word in ['deploy', 'code', 'release']):
            return "Our deployment process is solid! 🚀 Feature branch → code review (2 approvals) → tests → staging → QA → production (Tuesdays 2-4 AM). Safety first!"
        
        elif any(word in query for word in ['security', 'vpn', 'password']):
            return "Security is important! 🔒 Use VPN for remote access, change passwords every 90 days, enable 2FA everywhere. All data is encrypted. IT is here to help!"
        
        else:
            return "I can help with company info, work policies, benefits, expenses, design assets, deployment, and security! 😊 What would you like to know?"

class Handler(BaseHTTPRequestHandler):
    chatbot = SimpleChatbot()
    
    def do_GET(self):
        if self.path == '/':
            self.serve_file('index.html')
        elif self.path == '/style.css':
            self.serve_file('style.css')
        elif self.path == '/script.js':
            self.serve_file('script.js')
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/ask':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            question = data.get('question', '').strip()
            answer = self.chatbot.get_response(question) if question else "What would you like to know? 😊"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"answer": answer}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def serve_file(self, filename):
        try:
            with open(Path(__file__).parent / filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html' if filename.endswith('.html') else 'text/css' if filename.endswith('.css') else 'application/javascript')
            self.end_headers()
            self.wfile.write(content.encode())
        except:
            self.send_error(404)

if __name__ == "__main__":
    print("🤖 Starting Simple Chatbot on http://localhost:8080")
    HTTPServer(('localhost', 8080), Handler).serve_forever()