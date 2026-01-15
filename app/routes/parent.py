"""
Parent portal routes for Campus Connect
"""
from flask import Blueprint, request, jsonify, render_template
from app.services.supabase_service import SupabaseService
import asyncio

bp = Blueprint('parent', __name__)
supabase_service = SupabaseService()

# Page routes
@bp.route('/dashboard')
def dashboard():
    """Render parent dashboard"""
    return render_template('parentdashboard.html')

@bp.route('/academics')
def academics():
    """Render parent academics page"""
    return render_template('parentAcademics.html')

@bp.route('/attendance')
def attendance():
    """Render parent attendance page"""
    return render_template('parent-attendence.html')

@bp.route('/announcement')
def announcement():
    """Render parent announcement page"""
    return render_template('parent-announcement.html')

# API routes
@bp.route('/api/parent/<parent_id>/child')
def get_child_info(parent_id):
    """Get parent's child information"""
    try:
        result = asyncio.run(supabase_service.get_parent_child_info(parent_id))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/announcements')
def get_announcements():
    """Get announcements for parents"""
    try:
        role = request.args.get('role', 'parent')
        result = asyncio.run(supabase_service.get_announcements(role))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
