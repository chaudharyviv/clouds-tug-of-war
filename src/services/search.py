import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class SearchService:
    @staticmethod
    def search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Executes a web search using the Tavily API.
        """
        api_key = os.getenv("TAVILY_API_KEY")
        
        # If API key is missing or is the placeholder, return mock results
        if not api_key or api_key.startswith("tvly-"):
            print("WARNING: TAVILY_API_KEY is not set. Returning mock search results.")
            return SearchService._get_mock_results(query)
            
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=api_key)
            response = client.search(query=query, max_results=max_results, search_depth="advanced")
            return response.get("results", [])
        except Exception as e:
            print(f"Error during Tavily search: {e}")
            return SearchService._get_mock_results(query)

    @staticmethod
    def _get_mock_results(query: str) -> List[Dict[str, Any]]:
        """
        Returns mock search results for testing and demo purposes.
        """
        query_lower = query.lower()
        if "aws" in query_lower:
            return [
                {
                    "title": "AWS EC2 and Infrastructure Gravity",
                    "url": "https://aws.amazon.com/ec2/",
                    "content": "AWS has massive scale with millions of active customers, deep service depth (over 200 fully featured services), global reach across 30+ regions, but faces user complaints about complex pricing, egress charges, and heavy gravitational lock-in."
                },
                {
                    "title": "AWS Trainium and Inferentia AI Chips",
                    "url": "https://aws.amazon.com/machine-learning/trainium/",
                    "content": "AWS designs its own AI custom silicon like Trainium and Inferentia for cost-effective deep learning training. However, GPU supply constraints still affect on-demand allocation, and Nvidia H100/B200 GPU instances are heavily oversubscribed."
                }
            ]
        elif "coreweave" in query_lower:
            return [
                {
                    "title": "CoreWeave GPU Cloud Architecture",
                    "url": "https://www.coreweave.com/",
                    "content": "CoreWeave is an elite specialized NeoCloud offering massive clusters of NVIDIA H100, A100, and H200 GPUs. They deliver ultra-fast network interconnects (InfiniBand) and bare-metal performance, bypassing legacy virtualization layers for maximum training speed."
                },
                {
                    "title": "CoreWeave limitations and pricing",
                    "url": "https://www.coreweave.com/pricing",
                    "content": "CoreWeave has narrow service depth compared to hyperscalers, focused strictly on GPU workloads. They do not offer comprehensive database, edge routing, or global multi-region application deployment options. Pricing is direct and cheaper than hyperscalers for GPU compute."
                }
            ]
        elif "cloudflare" in query_lower:
            return [
                {
                    "title": "Cloudflare Workers Edge Platform",
                    "url": "https://workers.cloudflare.com/",
                    "content": "Cloudflare Workers run in over 300 edge locations worldwide with near-zero cold starts. Extremely strong at local latency, edge security, and lightweight serverless computing. However, they lack heavy centralized database persistence and cannot run large GPU training clusters."
                }
            ]
        elif "old fortress" in query_lower or "on-prem" in query_lower:
            return [
                {
                    "title": "On-Premises Data Center Resilience",
                    "url": "https://example.com/on-prem",
                    "content": "Traditional private clouds feature absolute control, complete compliance security, and zero egress fees. However, hardware procurement cycles take months, scaling takes forever, and operational simplicity is incredibly low compared to public clouds."
                }
            ]
        
        # General generic fallback
        return [
            {
                "title": f"Search Results for {query}",
                "url": "https://example.com/search",
                "content": f"Sourced capabilities and limitations of {query}. It is known for technical specializations and specific regional compliance advantages."
            }
        ]
