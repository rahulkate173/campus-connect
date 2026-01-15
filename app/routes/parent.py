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
