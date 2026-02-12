import { useState, useEffect } from 'react';
import {
    X,
    AlertTriangle,
    Clock,
    CheckCircle,
    User,
    Users,
    Calendar,
    ExternalLink,
    Play,
    Check,
    MessageSquare,
    Zap,
    Activity,
    Link,
    History,
    FileText,
    Loader2,
    Bell,
    BookOpen,
    Tag,
    ChevronDown,
    ChevronRight,
    Shield,
    Info
} from 'lucide-react';
import {
    fetchIncident,
    fetchIncidentLogEntries,
    fetchRelatedIncidents,
    fetchPastIncidents,
    acknowledgeIncident,
    resolveIncident,
    addIncidentNote
} from '../../services/api';
import './IncidentDetailModal.css';

export default function IncidentDetailModal({ incidentId, onClose }) {
    const [incident, setIncident] = useState(null);
    const [alerts, setAlerts] = useState([]);
    const [notes, setNotes] = useState([]);
    const [logEntries, setLogEntries] = useState([]);
    const [relatedIncidents, setRelatedIncidents] = useState([]);
    const [pastIncidents, setPastIncidents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('details');
    const [newNote, setNewNote] = useState('');
    const [addingNote, setAddingNote] = useState(false);
    const [actionLoading, setActionLoading] = useState(null);
    const [expandedAlerts, setExpandedAlerts] = useState({});

    useEffect(() => {
        if (incidentId) {
            loadIncidentData();
        }
    }, [incidentId]);

    async function loadIncidentData() {
        setLoading(true);
        try {
            // The enriched /api/incidents/{id} endpoint now returns alerts, notes, and log_entries too
            const [incidentData, relatedData, pastData] = await Promise.allSettled([
                fetchIncident(incidentId),
                fetchRelatedIncidents(incidentId),
                fetchPastIncidents(incidentId)
            ]);

            if (incidentData.status === 'fulfilled') {
                const data = incidentData.value;
                // enriched endpoint returns { incident, alerts, notes, log_entries }
                setIncident(data.incident || data);
                setAlerts(data.alerts || []);
                setNotes(data.notes || []);
                setLogEntries(data.log_entries || []);
            }
            if (relatedData.status === 'fulfilled') {
                setRelatedIncidents(relatedData.value.related_incidents || []);
            }
            if (pastData.status === 'fulfilled') {
                setPastIncidents(pastData.value.past_incidents || []);
            }
        } catch (err) {
            console.error('Error loading incident data:', err);
        } finally {
            setLoading(false);
        }
    }

    async function handleAcknowledge() {
        setActionLoading('acknowledge');
        try {
            await acknowledgeIncident(incidentId);
            await loadIncidentData();
        } catch (err) {
            console.error('Failed to acknowledge:', err);
        } finally {
            setActionLoading(null);
        }
    }

    async function handleResolve() {
        setActionLoading('resolve');
        try {
            await resolveIncident(incidentId);
            await loadIncidentData();
        } catch (err) {
            console.error('Failed to resolve:', err);
        } finally {
            setActionLoading(null);
        }
    }

    async function handleAddNote() {
        if (!newNote.trim()) return;
        setAddingNote(true);
        try {
            await addIncidentNote(incidentId, newNote);
            setNewNote('');
            await loadIncidentData();
        } catch (err) {
            console.error('Failed to add note:', err);
        } finally {
            setAddingNote(false);
        }
    }

    function toggleAlertExpanded(alertId) {
        setExpandedAlerts(prev => ({ ...prev, [alertId]: !prev[alertId] }));
    }

    function getStatusIcon(status) {
        switch (status) {
            case 'triggered':
                return <AlertTriangle size={20} className="status-icon critical" />;
            case 'acknowledged':
                return <Clock size={20} className="status-icon warning" />;
            case 'resolved':
                return <CheckCircle size={20} className="status-icon success" />;
            default:
                return <Activity size={20} className="status-icon" />;
        }
    }

    function formatTimestamp(timestamp) {
        if (!timestamp) return 'N/A';
        return new Date(timestamp).toLocaleString();
    }

    function renderCustomDetails(details) {
        if (!details || typeof details !== 'object') return null;

        return Object.entries(details).map(([key, value]) => {
            // Skip nested objects we render separately
            if (['labels', 'annotations', 'firing', 'resolved'].includes(key) && typeof value === 'object') return null;
            if (key === 'source' && typeof value === 'string' && value.length > 100) return null;

            return (
                <div key={key} className="custom-detail-row">
                    <span className="custom-detail-key">{key}:</span>
                    <span className="custom-detail-value">
                        {typeof value === 'string' ? value : JSON.stringify(value)}
                    </span>
                </div>
            );
        });
    }

    function renderLabels(labels) {
        if (!labels || typeof labels !== 'object') return null;
        return (
            <div className="labels-section">
                <h5><Tag size={14} /> Labels</h5>
                <div className="labels-grid">
                    {Object.entries(labels).map(([key, value]) => (
                        <div key={key} className="label-item">
                            <span className="label-key">{key}</span>
                            <span className="label-value">{value}</span>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    function renderAnnotations(annotations) {
        if (!annotations || typeof annotations !== 'object') return null;
        return (
            <div className="annotations-section">
                <h5><Info size={14} /> Annotations</h5>
                {Object.entries(annotations).map(([key, value]) => (
                    <div key={key} className="annotation-item">
                        <span className="annotation-key">{key}</span>
                        <span className="annotation-value">
                            {key.includes('url') || key.includes('URL') ? (
                                <a href={value} target="_blank" rel="noopener noreferrer">{value}</a>
                            ) : (
                                String(value)
                            )}
                        </span>
                    </div>
                ))}
            </div>
        );
    }

    if (!incidentId) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="incident-modal glass-card" onClick={(e) => e.stopPropagation()}>
                {/* Modal Header */}
                <div className="modal-header">
                    <div className="modal-title-row">
                        {incident && getStatusIcon(incident.status)}
                        <div className="modal-title-info">
                            <h2 className="modal-title">
                                {loading ? 'Loading...' : incident?.title || 'Incident Details'}
                            </h2>
                            <span className="modal-id">{incidentId}</span>
                        </div>
                    </div>
                    <button className="close-btn" onClick={onClose}>
                        <X size={24} />
                    </button>
                </div>

                {loading ? (
                    <div className="modal-loading">
                        <Loader2 size={48} className="spinner" />
                        <p>Loading incident details...</p>
                    </div>
                ) : (
                    <>
                        {/* Quick Actions */}
                        <div className="modal-actions">
                            {incident?.status === 'triggered' && (
                                <button
                                    className="btn btn-acknowledge"
                                    onClick={handleAcknowledge}
                                    disabled={actionLoading === 'acknowledge'}
                                >
                                    {actionLoading === 'acknowledge' ? (
                                        <Loader2 size={16} className="spinner" />
                                    ) : (
                                        <Play size={16} />
                                    )}
                                    Acknowledge
                                </button>
                            )}
                            {incident?.status !== 'resolved' && (
                                <button
                                    className="btn btn-resolve"
                                    onClick={handleResolve}
                                    disabled={actionLoading === 'resolve'}
                                >
                                    {actionLoading === 'resolve' ? (
                                        <Loader2 size={16} className="spinner" />
                                    ) : (
                                        <Check size={16} />
                                    )}
                                    Resolve
                                </button>
                            )}
                            {incident?.html_url && (
                                <a
                                    href={incident.html_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="btn btn-external"
                                >
                                    <ExternalLink size={16} />
                                    Open in PagerDuty
                                </a>
                            )}
                        </div>

                        {/* Tabs */}
                        <div className="modal-tabs">
                            <button
                                className={`tab ${activeTab === 'details' ? 'active' : ''}`}
                                onClick={() => setActiveTab('details')}
                            >
                                <FileText size={16} />
                                Details
                            </button>
                            <button
                                className={`tab ${activeTab === 'alerts' ? 'active' : ''}`}
                                onClick={() => setActiveTab('alerts')}
                            >
                                <Bell size={16} />
                                Alerts
                                {alerts.length > 0 && (
                                    <span className="tab-count">{alerts.length}</span>
                                )}
                            </button>
                            <button
                                className={`tab ${activeTab === 'timeline' ? 'active' : ''}`}
                                onClick={() => setActiveTab('timeline')}
                            >
                                <Activity size={16} />
                                Timeline
                                {logEntries.length > 0 && (
                                    <span className="tab-count">{logEntries.length}</span>
                                )}
                            </button>
                            <button
                                className={`tab ${activeTab === 'notes' ? 'active' : ''}`}
                                onClick={() => setActiveTab('notes')}
                            >
                                <MessageSquare size={16} />
                                Notes
                                {notes.length > 0 && (
                                    <span className="tab-count">{notes.length}</span>
                                )}
                            </button>
                            <button
                                className={`tab ${activeTab === 'related' ? 'active' : ''}`}
                                onClick={() => setActiveTab('related')}
                            >
                                <Link size={16} />
                                Related
                                {relatedIncidents.length > 0 && (
                                    <span className="tab-count">{relatedIncidents.length}</span>
                                )}
                            </button>
                            <button
                                className={`tab ${activeTab === 'past' ? 'active' : ''}`}
                                onClick={() => setActiveTab('past')}
                            >
                                <History size={16} />
                                Past
                                {pastIncidents.length > 0 && (
                                    <span className="tab-count">{pastIncidents.length}</span>
                                )}
                            </button>
                        </div>

                        {/* Tab Content */}
                        <div className="modal-content">
                            {activeTab === 'details' && (
                                <div className="details-tab">
                                    <div className="detail-grid">
                                        <div className="detail-item">
                                            <span className="detail-label">Severity</span>
                                            <span className={`detail-value badge badge-${incident?.urgency === 'high' ? 'critical' : 'medium'}`}>
                                                {incident?.urgency === 'high' ? 'Critical' : 'Medium'}
                                            </span>
                                        </div>
                                        <div className="detail-item">
                                            <span className="detail-label">Opened</span>
                                            <span className="detail-value">
                                                {incident?.created_at ? formatTimestamp(incident.created_at) : 'Unknown'}
                                            </span>
                                        </div>
                                        <div className="detail-item">
                                            <span className="detail-label">Alert Key</span>
                                            <span className="detail-value monospace">
                                                {incident?.incident_key || incident?.id || 'N/A'}
                                            </span>
                                        </div>
                                        <div className="detail-item">
                                            <span className="detail-label">Current Status</span>
                                            <span className={`detail-value badge badge-${incident?.status}`}>
                                                {incident?.status}
                                            </span>
                                        </div>
                                        <div className="detail-item full-width">
                                            <span className="detail-label">Service Name</span>
                                            <span className="detail-value highlight">
                                                {incident?.service?.summary || 'Unknown Service'}
                                            </span>
                                        </div>
                                        {incident?.escalation_policy && (
                                            <div className="detail-item full-width">
                                                <span className="detail-label">Escalation Policy</span>
                                                <span className="detail-value">
                                                    {incident.escalation_policy.summary || 'N/A'}
                                                </span>
                                            </div>
                                        )}
                                        {incident?.last_status_change_at && (
                                            <div className="detail-item full-width">
                                                <span className="detail-label">Last Status Change</span>
                                                <span className="detail-value">
                                                    {formatTimestamp(incident.last_status_change_at)}
                                                    {incident?.last_status_change_by?.summary && (
                                                        <> by <strong>{incident.last_status_change_by.summary}</strong></>
                                                    )}
                                                </span>
                                            </div>
                                        )}
                                    </div>

                                    {/* Details Section */}
                                    <div className="detail-section pagerduty-details">
                                        <h4>Details</h4>
                                        <div className="details-content">
                                            <div className="detail-row">
                                                <span className="detail-label">SUBJECT</span>
                                                <span className="detail-value">{incident?.title || 'No subject'}</span>
                                            </div>
                                            {incident?.body?.details && (
                                                <div className="detail-row">
                                                    <span className="detail-label">DETAILS</span>
                                                    <pre className="detail-value body-text">{incident.body.details}</pre>
                                                </div>
                                            )}
                                            {incident?.description && (
                                                <div className="detail-row">
                                                    <span className="detail-label">BODY</span>
                                                    <pre className="detail-value body-text">{incident.description}</pre>
                                                </div>
                                            )}
                                        </div>
                                    </div>

                                    {incident?.assignments?.length > 0 && (
                                        <div className="detail-section">
                                            <h4>Assigned To</h4>
                                            <div className="assignees-list">
                                                {incident.assignments.map((assignment, idx) => (
                                                    <div key={idx} className="assignee-item">
                                                        <User size={16} />
                                                        <span>{assignment.assignee?.summary || 'Unknown'}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Quick Alert Summary at bottom of details */}
                                    {alerts.length > 0 && (
                                        <div className="detail-section alert-summary-section">
                                            <h4><Bell size={16} /> Alert Summary ({alerts.length})</h4>
                                            <p className="alert-hint">View the <strong>Alerts</strong> tab for full custom details, labels, and annotations.</p>
                                            {alerts.slice(0, 3).map((alert, idx) => (
                                                <div key={idx} className="alert-summary-item">
                                                    <span className={`alert-status-dot status-${alert.status}`}></span>
                                                    <span className="alert-summary-text">
                                                        {alert.summary || alert.id}
                                                    </span>
                                                    <span className={`badge badge-${alert.severity === 'critical' ? 'critical' : 'medium'}`}>
                                                        {alert.severity || 'info'}
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* ALERTS TAB - Full Custom Details like PagerDuty Portal */}
                            {activeTab === 'alerts' && (
                                <div className="alerts-tab">
                                    {alerts.length === 0 ? (
                                        <div className="empty-tab">
                                            <Bell size={48} />
                                            <p>No alerts found for this incident</p>
                                        </div>
                                    ) : (
                                        <div className="alerts-list">
                                            {alerts.map((alert, idx) => {
                                                const isExpanded = expandedAlerts[alert.id] !== false; // default expanded
                                                const body = alert.body || {};
                                                const details = alert.custom_details || body.details || {};
                                                const labels = alert.labels || (typeof details === 'object' ? details.labels : null) || {};
                                                const annotations = alert.annotations || (typeof details === 'object' ? details.annotations : null) || {};
                                                const firing = typeof details === 'object' ? (details.firing || '') : '';
                                                const runbookUrl = alert.runbook_url || (annotations.runbook_url) || '';
                                                const silenceUrl = typeof details === 'object' ? (details.SilenceURL || details.silence_url || '') : '';
                                                const contexts = body.contexts || [];

                                                return (
                                                    <div key={idx} className={`alert-card ${alert.status}`}>
                                                        <div className="alert-header" onClick={() => toggleAlertExpanded(alert.id)}>
                                                            <div className="alert-header-left">
                                                                {isExpanded ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
                                                                <span className={`alert-status-badge status-${alert.status}`}>
                                                                    {alert.status?.toUpperCase()}
                                                                </span>
                                                                <span className={`alert-severity-badge severity-${alert.severity}`}>
                                                                    {alert.severity || 'info'}
                                                                </span>
                                                            </div>
                                                            <span className="alert-summary-title">
                                                                {alert.summary || 'Alert'}
                                                            </span>
                                                            <span className="alert-time">
                                                                {formatTimestamp(alert.created_at)}
                                                            </span>
                                                        </div>

                                                        {isExpanded && (
                                                            <div className="alert-body">
                                                                {/* Custom Details / Firing Info */}
                                                                {typeof firing === 'string' && firing && (
                                                                    <div className="alert-section">
                                                                        <h5>Custom Details</h5>
                                                                        <div className="firing-block">
                                                                            <div className="firing-label">firing:</div>
                                                                            <pre className="firing-content">{firing}</pre>
                                                                        </div>
                                                                    </div>
                                                                )}

                                                                {/* Labels */}
                                                                {typeof labels === 'object' && Object.keys(labels).length > 0 && (
                                                                    renderLabels(labels)
                                                                )}

                                                                {/* Annotations */}
                                                                {typeof annotations === 'object' && Object.keys(annotations).length > 0 && (
                                                                    renderAnnotations(annotations)
                                                                )}

                                                                {/* Firing/Resolved counts */}
                                                                {(alert.num_firing !== undefined || alert.num_resolved !== undefined) && (
                                                                    <div className="alert-counts">
                                                                        <div className="count-item firing">
                                                                            <span className="count-label">num_firing:</span>
                                                                            <span className="count-value">{alert.num_firing ?? 0}</span>
                                                                        </div>
                                                                        <div className="count-item resolved">
                                                                            <span className="count-label">num_resolved:</span>
                                                                            <span className="count-value">{alert.num_resolved ?? 0}</span>
                                                                        </div>
                                                                    </div>
                                                                )}

                                                                {/* Runbook URL */}
                                                                {runbookUrl && (
                                                                    <div className="alert-link-section">
                                                                        <BookOpen size={14} />
                                                                        <a href={runbookUrl} target="_blank" rel="noopener noreferrer">
                                                                            Runbook: {runbookUrl}
                                                                        </a>
                                                                    </div>
                                                                )}

                                                                {/* Silence URL */}
                                                                {silenceUrl && (
                                                                    <div className="alert-link-section">
                                                                        <Shield size={14} />
                                                                        <a href={silenceUrl} target="_blank" rel="noopener noreferrer">
                                                                            Silence URL: {silenceUrl}
                                                                        </a>
                                                                    </div>
                                                                )}

                                                                {/* Alert Key */}
                                                                {alert.alert_key && (
                                                                    <div className="alert-key-section">
                                                                        <span className="alert-key-label">Alert Key:</span>
                                                                        <code className="alert-key-value">{alert.alert_key}</code>
                                                                    </div>
                                                                )}

                                                                {/* Context Links */}
                                                                {contexts.length > 0 && (
                                                                    <div className="alert-contexts">
                                                                        {contexts.map((ctx, cidx) => (
                                                                            <a key={cidx} href={ctx.href} target="_blank" rel="noopener noreferrer" className="context-link">
                                                                                <ExternalLink size={12} />
                                                                                {ctx.text || 'View'}
                                                                            </a>
                                                                        ))}
                                                                    </div>
                                                                )}

                                                                {/* Source */}
                                                                {typeof details === 'object' && details.source && (
                                                                    <div className="alert-source">
                                                                        <span className="source-label">Source:</span>
                                                                        <code className="source-value">{String(details.source).substring(0, 200)}</code>
                                                                    </div>
                                                                )}
                                                            </div>
                                                        )}
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    )}
                                </div>
                            )}

                            {activeTab === 'timeline' && (
                                <div className="timeline-tab">
                                    {logEntries.length === 0 ? (
                                        <div className="empty-tab">
                                            <Activity size={48} />
                                            <p>No log entries found</p>
                                        </div>
                                    ) : (
                                        <div className="timeline-list">
                                            {logEntries.map((entry, idx) => (
                                                <div key={idx} className="timeline-item">
                                                    <div className="timeline-dot"></div>
                                                    <div className="timeline-content">
                                                        <span className="timeline-type">{entry.type}</span>
                                                        <span className="timeline-summary">
                                                            {entry.summary || entry.channel?.summary || 'Action performed'}
                                                        </span>
                                                        <span className="timeline-time">
                                                            {formatTimestamp(entry.created_at)}
                                                        </span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* NOTES TAB */}
                            {activeTab === 'notes' && (
                                <div className="notes-tab">
                                    {/* Add Note Form */}
                                    <div className="add-note-form">
                                        <textarea
                                            value={newNote}
                                            onChange={(e) => setNewNote(e.target.value)}
                                            placeholder="Type a note to add to this incident..."
                                            rows={3}
                                        />
                                        <button
                                            className="btn btn-primary"
                                            onClick={handleAddNote}
                                            disabled={!newNote.trim() || addingNote}
                                        >
                                            {addingNote ? (
                                                <Loader2 size={16} className="spinner" />
                                            ) : (
                                                <MessageSquare size={16} />
                                            )}
                                            Add Note
                                        </button>
                                    </div>

                                    {notes.length === 0 ? (
                                        <div className="empty-tab">
                                            <MessageSquare size={48} />
                                            <p>No notes yet. Add a note above.</p>
                                        </div>
                                    ) : (
                                        <div className="notes-list">
                                            {notes.map((note, idx) => (
                                                <div key={idx} className="note-item">
                                                    <div className="note-header">
                                                        <User size={14} />
                                                        <span className="note-author">
                                                            {note.user?.summary || 'Unknown'}
                                                        </span>
                                                        <span className="note-time">
                                                            {formatTimestamp(note.created_at)}
                                                        </span>
                                                    </div>
                                                    <div className="note-content">{note.content}</div>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}

                            {activeTab === 'related' && (
                                <div className="related-tab">
                                    {relatedIncidents.length === 0 ? (
                                        <div className="empty-tab">
                                            <Link size={48} />
                                            <p>No related incidents found</p>
                                            <span className="empty-hint">This feature requires PagerDuty AIOps add-on</span>
                                        </div>
                                    ) : (
                                        <div className="incidents-list">
                                            {relatedIncidents.map((inc, idx) => (
                                                <div key={idx} className="incident-item">
                                                    <div className={`incident-status-dot status-${inc.status}`}></div>
                                                    <div className="incident-item-info">
                                                        <span className="incident-item-title">{inc.title}</span>
                                                        <span className="incident-item-meta">
                                                            {inc.service?.summary} • {formatTimestamp(inc.created_at)}
                                                        </span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}

                            {activeTab === 'past' && (
                                <div className="past-tab">
                                    {pastIncidents.length === 0 ? (
                                        <div className="empty-tab">
                                            <History size={48} />
                                            <p>No past incidents found</p>
                                            <span className="empty-hint">This feature requires PagerDuty AIOps add-on</span>
                                        </div>
                                    ) : (
                                        <div className="incidents-list">
                                            {pastIncidents.map((inc, idx) => (
                                                <div key={idx} className="incident-item">
                                                    <div className={`incident-status-dot status-${inc.status}`}></div>
                                                    <div className="incident-item-info">
                                                        <span className="incident-item-title">{inc.title}</span>
                                                        <span className="incident-item-meta">
                                                            {inc.service?.summary} • {formatTimestamp(inc.created_at)}
                                                        </span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}
