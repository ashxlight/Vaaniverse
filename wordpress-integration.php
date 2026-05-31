<?php
/**
 * Vaaniverse RAG Chat WordPress Plugin
 * Version: 1.0
 *
 * Installation:
 * 1. Create folder: wp-content/plugins/vaaniverse-rag-chat/
 * 2. Copy this file as: vaaniverse-rag-chat.php
 * 3. Go to WordPress Admin → Plugins → Activate "Vaaniverse RAG Chat"
 * 4. Chatbot appears on all pages automatically
 */

// ─────────────────────────────────────────────
// PLUGIN HEADER
// ─────────────────────────────────────────────
/*
Plugin Name: Vaaniverse RAG Chat
Plugin URI: https://vaaniverse.com
Description: AI-powered chatbot for Vaaniverse - answers questions about services, pricing, and how we help
Version: 1.0.0
Author: Vaaniverse
Author URI: https://vaaniverse.com
License: GPL v3
Text Domain: vaaniverse-rag
*/

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// ─────────────────────────────────────────────
// ENQUEUE CHATBOT
// ─────────────────────────────────────────────
add_action('wp_footer', 'vaaniverse_rag_enqueue', 999);

function vaaniverse_rag_enqueue() {
    // Don't show to logged-in users (optional)
    // if (is_user_logged_in()) return;

    // Get the chatbot widget HTML
    $widget_path = plugin_dir_path(__FILE__) . 'rag-chatbot-widget.html';

    if (!file_exists($widget_path)) {
        return; // Widget file not found
    }

    // Read and output widget
    $widget_html = file_get_contents($widget_path);

    // Replace backend URL with your Railway deployment
    $backend_url = 'https://your-railway-url.railway.app'; // CHANGE THIS
    $widget_html = str_replace(
        "backendUrl: 'http://localhost:5000'",
        "backendUrl: '" . esc_attr($backend_url) . "'",
        $widget_html
    );

    echo $widget_html;
}

// ─────────────────────────────────────────────
// PLUGIN SETTINGS PAGE (OPTIONAL)
// ─────────────────────────────────────────────
add_action('admin_menu', 'vaaniverse_rag_add_settings_menu');

function vaaniverse_rag_add_settings_menu() {
    add_options_page(
        'Vaaniverse RAG Chat Settings',
        'Vaaniverse Chat',
        'manage_options',
        'vaaniverse-rag-settings',
        'vaaniverse_rag_settings_page'
    );
}

function vaaniverse_rag_settings_page() {
    ?>
    <div class="wrap">
        <h1>Vaaniverse RAG Chat Settings</h1>
        <form method="post" action="options.php">
            <?php settings_fields('vaaniverse_rag_settings'); ?>
            <table class="form-table">
                <tr>
                    <th scope="row">
                        <label for="vaaniverse_backend_url">Backend API URL</label>
                    </th>
                    <td>
                        <input
                            type="url"
                            id="vaaniverse_backend_url"
                            name="vaaniverse_backend_url"
                            value="<?php echo esc_attr(get_option('vaaniverse_backend_url', '')); ?>"
                            class="regular-text"
                            placeholder="https://your-railway-url.railway.app"
                        />
                        <p class="description">
                            Your Railway deployment URL.
                            <a href="https://railway.app" target="_blank">Get your URL from Railway</a>
                        </p>
                    </td>
                </tr>
                <tr>
                    <th scope="row">
                        <label for="vaaniverse_show_logged_in">Show to Logged-in Users</label>
                    </th>
                    <td>
                        <input
                            type="checkbox"
                            id="vaaniverse_show_logged_in"
                            name="vaaniverse_show_logged_in"
                            value="1"
                            <?php checked(get_option('vaaniverse_show_logged_in'), 1); ?>
                        />
                        <label for="vaaniverse_show_logged_in">
                            Enable chatbot for logged-in users too
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">
                        <label for="vaaniverse_enable_chat">Enable Chatbot</label>
                    </th>
                    <td>
                        <input
                            type="checkbox"
                            id="vaaniverse_enable_chat"
                            name="vaaniverse_enable_chat"
                            value="1"
                            <?php checked(get_option('vaaniverse_enable_chat', 1), 1); ?>
                        />
                        <label for="vaaniverse_enable_chat">
                            Turn chatbot on/off globally
                        </label>
                    </td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>

        <hr/>

        <h2>Documentation</h2>
        <p>
            <a href="https://vaaniverse.com/rag-chatbot-setup.md" target="_blank">
                View Full Setup Guide
            </a>
        </p>
        <p>
            <strong>To get started:</strong>
        </p>
        <ol>
            <li>Deploy backend to <a href="https://railway.app" target="_blank">Railway</a></li>
            <li>Copy your Railway URL above</li>
            <li>Save settings</li>
            <li>Chatbot appears on your site!</li>
        </ol>
    </div>
    <?php
}

// Register settings
add_action('admin_init', 'vaaniverse_rag_register_settings');

function vaaniverse_rag_register_settings() {
    register_setting('vaaniverse_rag_settings', 'vaaniverse_backend_url');
    register_setting('vaaniverse_rag_settings', 'vaaniverse_show_logged_in');
    register_setting('vaaniverse_rag_settings', 'vaaniverse_enable_chat');
}

// ─────────────────────────────────────────────
// UPDATE ENQUEUE WITH SETTINGS
// ─────────────────────────────────────────────
remove_action('wp_footer', 'vaaniverse_rag_enqueue', 999);
add_action('wp_footer', 'vaaniverse_rag_enqueue_with_settings', 999);

function vaaniverse_rag_enqueue_with_settings() {
    // Check if enabled
    if (!get_option('vaaniverse_enable_chat', 1)) {
        return;
    }

    // Check logged-in status
    if (is_user_logged_in() && !get_option('vaaniverse_show_logged_in')) {
        return;
    }

    // Get backend URL from settings
    $backend_url = get_option('vaaniverse_backend_url', 'http://localhost:5000');

    if (empty($backend_url)) {
        return; // No backend URL configured
    }

    // Get the chatbot widget HTML
    $widget_path = plugin_dir_path(__FILE__) . 'rag-chatbot-widget.html';

    if (!file_exists($widget_path)) {
        return;
    }

    // Read and output widget
    $widget_html = file_get_contents($widget_path);

    // Replace backend URL
    $widget_html = str_replace(
        "backendUrl: 'http://localhost:5000'",
        "backendUrl: '" . esc_attr($backend_url) . "'",
        $widget_html
    );

    echo $widget_html;
}

// ─────────────────────────────────────────────
// ACTIVATION HOOK
// ─────────────────────────────────────────────
register_activation_hook(__FILE__, 'vaaniverse_rag_activate');

function vaaniverse_rag_activate() {
    // Set default options
    if (!get_option('vaaniverse_enable_chat')) {
        add_option('vaaniverse_enable_chat', 1);
    }
}

// ─────────────────────────────────────────────
// DEACTIVATION HOOK (OPTIONAL)
// ─────────────────────────────────────────────
register_deactivation_hook(__FILE__, 'vaaniverse_rag_deactivate');

function vaaniverse_rag_deactivate() {
    // Cleanup if needed
    // delete_option('vaaniverse_backend_url');
}

?>
