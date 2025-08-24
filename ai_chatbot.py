from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse
from pathlib import Path

class AIChatbot:
    def __init__(self):
        self.company_context = """
        You are a helpful internal company assistant. Here's our company information:
        
        COMPANY: We're a technology company building innovative solutions. Mission: make technology accessible.
        
        WORK HOURS: 9 AM-5 PM EST, flexible scheduling available, remote work 3 days/week, core hours 10 AM-3 PM EST
        
        BENEFITS: 100% health insurance covered, dental & vision, 401k matching 6%, 25 days vacation + 10 sick days, $3K professional development budget, $100/month gym reimbursement
        
        EXPENSES: Reimbursed within 30 days, receipts required >$25, travel fully covered, home office setup $1.5K, entertainment $200/month limit
        
        DESIGN: Brand guidelines at wiki.company.com/brand, logos in /Marketing/Brand, requests to design@company.com, 3-5 day turnaround
        
        DEPLOYMENT: Feature branch → code review (2 approvals) → tests → staging → QA → production (Tuesdays 2-4 AM EST) → monitor 24hrs
        
        SECURITY: VPN required for remote access, passwords change every 90 days, 2FA mandatory, AES-256 encryption, HTTPS required
        
        Always be friendly, helpful, and conversational. Use emojis appropriately. Give specific, actionable answers.
        """
        print("AI Chatbot initialized with company context")
    
    def get_ai_response(self, query):
        """Get response from free AI API"""
        try:
            # Using Hugging Face Inference API (free)
            prompt = f"{self.company_context}\n\nEmployee Question: {query}\n\nHelpful Response:"
            
            # Prepare the request
            data = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            # Make request to Hugging Face API
            req = urllib.request.Request(
                "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                data=json.dumps(data).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer hf_demo'  # Demo token - replace with your own
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').strip()
                    
        except Exception as e:
            print(f"AI API error: {e}")
            
        # Fallback to rule-based responses if AI fails
        return self.get_fallback_response(query)
    
    def get_fallback_response(self, query):
        """Fallback responses when AI is unavailable"""
        query = query.lower().strip()
        print(f"DEBUG: Processing query: '{query}'")
        
        if any(word in query for word in ['hello', 'hi', 'hey']):
            print("DEBUG: Matched greeting")
            return "Hey there! 👋 I'm your AI-powered company assistant. What can I help you with today?"
        
        elif any(word in query for word in ['company', 'about', 'what is']):
            return "We're a tech company building innovative solutions! 🚀 We focus on making technology accessible and useful for everyone. Our culture emphasizes work-life balance and professional growth. Want to know about specific aspects like benefits or work policies?"
        
        elif any(word in query for word in ['work', 'hours', 'remote']):
            return "Here's our flexible work setup! ⏰ Standard hours are 9 AM-5 PM EST, but we're quite flexible with manager approval. Remote work is supported 3 days per week with core collaboration hours from 10 AM-3 PM EST. We really believe in work-life balance! 🏡"
        
        elif any(word in query for word in ['benefits', 'insurance', 'vacation']):
            return "Our benefits package is comprehensive! 🎉 We cover 100% of health insurance premiums plus dental & vision, offer 401k matching up to 6%, provide 25 days vacation plus 10 sick days, give a $3K annual professional development budget, and reimburse $100/month for gym memberships. We really invest in our people! 💪"
        
        elif any(word in query for word in ['refund', 'expense', 'reimburse']):
            return "Expense reimbursement is straightforward! 💰 Submit receipts within 30 days and you'll get reimbursed. We require receipts for expenses over $25. Travel expenses (flights, hotels, meals) are fully covered, home office setup gets up to $1.5K reimbursement, and there's a $200 monthly limit for client entertainment. Just keep those receipts! 📄"
        
        elif any(word in query for word in ['design', 'logo', 'brand']):
            return "Need design assets? 🎨 You can find our brand guidelines at wiki.company.com/brand, logo files are in the shared drive at /Marketing/Brand, or submit custom requests to design@company.com. Our design team typically has a 3-5 day turnaround and they're super helpful! ✨"
        
        elif any(word in query for word in ['deploy', 'code', 'release']):
            return "Our deployment process prioritizes safety! 🚀 Here's the flow: Create feature branch → get code review with minimum 2 approvals → run automated tests → deploy to staging → get QA testing and approval → deploy to production during maintenance window (Tuesdays 2-4 AM EST) → monitor for 24 hours. We'd rather be safe than sorry! 🛡️"
        
        elif any(word in query for word in ['security', 'vpn', 'password']):
            return "Security is super important to us! 🔒 You'll need VPN for all remote access, passwords must be changed every 90 days, two-factor authentication is mandatory for all accounts, all our data is encrypted at rest with AES-256, and HTTPS is required for all endpoints. IT is always available to help with any security questions! 🛡️"
        
        else:
            return "I'm your AI-powered assistant and I can help with lots of company topics! 😊 I can answer questions about our work policies, benefits, expense reimbursement, design assets, deployment processes, security requirements, and much more. What would you like to know about? 🤔"
    
    def get_response(self, query):
        """Main response method - uses fallback responses for better control"""
        if not query.strip():
            return "Hi there! What would you like to know about our company? 😊"
        
        # Use fallback responses directly for consistent, friendly responses
        return self.get_fallback_response(query)

class Handler(BaseHTTPRequestHandler):
    chatbot = AIChatbot()
    
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
            answer = self.chatbot.get_response(question)
            
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
    print("Starting AI-Powered Chatbot on http://localhost:8080")
    print("Using AI for intelligent responses with company context")
    HTTPServer(('localhost', 8080), Handler).serve_forever()