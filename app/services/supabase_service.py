"""
Supabase service layer for Campus Connect
Handles all database operations with Supabase
"""
import os
from typing import Optional, Dict, List, Any
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseService:
    """Service class for Supabase operations"""
    
    def __init__(self):
        """Initialize Supabase client"""
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.client: Client = create_client(url, key)
    
    # Authentication methods
    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in user with email and password"""
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return {"success": True, "data": response}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def sign_out(self) -> Dict[str, Any]:
        """Sign out current user"""
        try:
            self.client.auth.sign_out()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current authenticated user"""
        try:
            user = self.client.auth.get_user()
            return user
        except Exception as e:
            return None
    
    # Profile operations
    async def get_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile by user_id"""
        try:
            response = self.client.table("profiles").select("*").eq("id", user_id).execute()
            if response.data:
                return {"success": True, "data": response.data[0]}
            return {"success": False, "error": "Profile not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_profile(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        try:
            response = self.client.table("profiles").update(data).eq("id", user_id).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Classroom operations
    async def get_all_classrooms(self) -> Dict[str, Any]:
        """Get all classrooms"""
        try:
            response = self.client.table("classrooms").select("*").execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_classroom_by_year(self, class_year: str) -> Dict[str, Any]:
        """Get classroom by year"""
        try:
            response = self.client.table("classrooms").select("*").eq("class_year", class_year).execute()
            if response.data:
                return {"success": True, "data": response.data[0]}
            return {"success": False, "error": "Classroom not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_timetable(self, class_year: str) -> Dict[str, Any]:
        """Get timetable for a classroom"""
        try:
            response = self.client.table("classrooms").select("timetable").eq("class_year", class_year).execute()
            if response.data:
                return {"success": True, "data": response.data[0].get("timetable", {})}
            return {"success": False, "error": "Timetable not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_timetable(self, class_year: str, timetable: Dict[str, Any]) -> Dict[str, Any]:
        """Update timetable for a classroom"""
        try:
            response = self.client.table("classrooms").update({"timetable": timetable}).eq("class_year", class_year).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Attendance operations
    async def get_student_attendance(self, student_id: str) -> Dict[str, Any]:
        """Get attendance records for a student"""
        try:
            response = self.client.table("attendance").select("*").eq("student_id", student_id).execute()
            
            # Calculate overall percentage
            total = len(response.data)
            if total > 0:
                present_count = sum(1 for record in response.data 
                                  if record.get("periods", {}).get("status") == "present")
                percentage = (present_count / total) * 100
            else:
                percentage = 0
            
            return {
                "success": True,
                "data": response.data,
                "overall_percentage": round(percentage, 2),
                "total_records": total
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def create_attendance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create attendance record"""
        try:
            response = self.client.table("attendance").insert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_attendance(self, attendance_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update attendance record"""
        try:
            response = self.client.table("attendance").update(data).eq("id", attendance_id).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Assignment operations
    async def get_assignments(self, classroom_id: str) -> Dict[str, Any]:
        """Get assignments for a classroom"""
        try:
            response = self.client.table("assignments").select("*").eq("classroom_id", classroom_id).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def create_assignment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create assignment"""
        try:
            response = self.client.table("assignments").insert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_assignment(self, assignment_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update assignment"""
        try:
            response = self.client.table("assignments").update(data).eq("id", assignment_id).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def delete_assignment(self, assignment_id: str) -> Dict[str, Any]:
        """Delete assignment"""
        try:
            response = self.client.table("assignments").delete().eq("id", assignment_id).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Marks operations
    async def get_student_marks(self, student_id: str) -> Dict[str, Any]:
        """Get marks for a student"""
        try:
            response = self.client.table("marks").select("*").eq("student_id", student_id).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def create_marks(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create marks record"""
        try:
            response = self.client.table("marks").insert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_marks(self, mark_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update marks record"""
        try:
            response = self.client.table("marks").update(data).eq("id", mark_id).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Announcement operations
    async def get_announcements(self, role: Optional[str] = None) -> Dict[str, Any]:
        """Get announcements with optional role filter"""
        try:
            query = self.client.table("announcements").select("*")
            if role:
                query = query.eq("role", role)
            response = query.execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def create_announcement(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create announcement"""
        try:
            response = self.client.table("announcements").insert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def delete_announcement(self, announcement_id: str) -> Dict[str, Any]:
        """Delete announcement"""
        try:
            response = self.client.table("announcements").delete().eq("id", announcement_id).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Student and Parent operations
    async def get_students_by_class(self, class_year: str) -> Dict[str, Any]:
        """Get students by class year"""
        try:
            response = self.client.table("profiles").select("*").eq("role", "student").eq("class_year", class_year).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_parent_child_info(self, parent_id: str) -> Dict[str, Any]:
        """Get parent's child information"""
        try:
            # First get parent profile to find child_id
            parent_response = self.client.table("profiles").select("*").eq("id", parent_id).execute()
            if not parent_response.data:
                return {"success": False, "error": "Parent not found"}
            
            parent = parent_response.data[0]
            child_id = parent.get("child_id")
            
            if not child_id:
                return {"success": False, "error": "No child linked to this parent"}
            
            # Get child profile
            child_response = self.client.table("profiles").select("*").eq("id", child_id).execute()
            if not child_response.data:
                return {"success": False, "error": "Child not found"}
            
            return {"success": True, "data": child_response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
